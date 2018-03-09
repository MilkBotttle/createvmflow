from viewflow.activation import * 
from viewflow import mixins, Event, ThisObject
from django.utils.decorators import method_decorator
from viewflow.decorators import flow_start_func
from viewflow.flow import views
from viewflow import Task
# Subprocess    
class SubProcessActivation(Activation):
    """
    .. graphviz::
       
       digraph status {
            UNPRIE;
            NEW -> CANCELED [label="cancel"]
            NEW -> PREPARED [label="prepare"]
            PREPARED -> INSUBPROGRESS [label="progress"]
            INSUBPROCESS -> DONE [label="done"]
            DONE -> NEW [label="undo"]
            {rank = min;NEW}            
       }
    """
    
    @Activation.status.transition(source=STATUS.NEW, target=STATUS.PREPARED)
    def prepare(self):
        if self.task.started is None:
            self.task.started = now()

        signals.task_started.send(
            sender=self.flow_class,
            process=self.process,
            task=self.task)

    @Activation.status.transition(source=STATUS.PREPARED, target=STATUS.INSUBPROGRESS)
    def progress(self):
        """Perform the subprocess"""
        #start subprocess 
        self.process.status = STATUS.INSUBPROGRESS
        self.process.save()
        self.flow_task._subprocess_start.start(self.process, self.task)

    @Activation.status.transition(source=STATUS.DONE, conditions=[all_leading_canceled])
    def activate_next(self):
        """Activate all outgoing edges."""

        if self.flow_task._next:
            self.flow_task._next.activate(
                prev_activation=self, token=self.task.token)

    @Activation.status.transition(source=STATUS.INSUBPROGRESS, target=STATUS.DONE)
    def done(self):
        self.task.finished = now()
        self.set_status(STATUS.DONE)
        self.task.save()

        signals.task_finished.send(
            sender=self.flow_class,
            process=self.process,
            task=self.task)

        self.activate_next()

    @classmethod
    def activate(cls, flow_task, prev_activation, token):
        """
            new a task
            return activation
            
        """
        task = flow_task.flow_class.task_class(
            process=prev_activation.process,
            flow_task=flow_task,
            token=token)

        task.save()
        task.previous.add(prev_activation.task)

        activation = cls()
        activation.initialize(flow_task, task)
        activation.prepare()
        activation.progress()
        return activation

    def is_done(self):
        """
            Check all subprocess are 'DONE', return boolean
        """
        subprocess_class = self.flow_task._subprocess_start.flow_class.process_class
        subprocesses = subprocess_class._default_manager.filter(parent_task=self.task).exclude(status=STATUS.DONE).exists()
        return not subprocesses
    
    @Activation.status.transition(source=STATUS.DONE, target=STATUS.NEW)
    def undo(self):
        pass

class SubProcess(mixins.TaskDescriptionMixin,
                 mixins.NextNodeMixin,
                 mixins.DetailViewMixin,
                 mixins.UndoViewMixin,
                 mixins.CancelViewMixin,
                 mixins.PerformViewMixin,
                 Task):
    """
        start_sub = (
            SubProcess(subprocess.start)
                .Next(this.end)
        )
    """
    task_type = 'SUBPROCESS'
    activation_class = SubProcessActivation
    
    cancel_view_class = views.CancelTaskView
    detail_view_class = views.DetailTaskView
    perform_view_class = views.PerformTaskView
    undo_view_class = views.UndoTaskView

    def __init__(self, subprocess_start, **kwargs):
        """
        Instantiate a SubProcess node.
        
        :keyword subprocess_start: A StarSubProcess task
        """
        self._subprocess_start = subprocess_start
        super(SubProcess, self).__init__(**kwargs)

    def on_subprocess_end(self, **signal_kwargs):
        process = signal_kwargs['process']                  

        if process.parent_task:                             
            activation = self.activation_class()              
            activation.initialize(self, process.parent_task)
            if activation.is_done():
                #Cameron.c : set the status to insubprogress to transition
                activation.set_status(STATUS.INSUBPROGRESS)
                activation.done()
    
    def ready(self, **singnal_args):
        """
            connect subprocess finished signal to here
        """
        signals.flow_finished.connect(self.on_subprocess_end, sender=self._subprocess_start.flow_class) 

class StartSubProcessActivaton(StartActivation):
    """ Start a new subprocess """

    @Activation.status.transition(source=STATUS.NEW, target=STATUS.PREPARED)
    def prepare(self,parent_process,parent_task):
        if self.task.started is None:
            self.task.started = now()
        self.process.parent_process = parent_process
        self.process.parent_task = parent_task

    @Activation.status.transition(source=STATUS.DONE, conditions=[all_leading_canceled])
    def activate_next(self):
        if self.flow_task._next:
            self.flow_task._next.activate(
                prev_activation=self, token=self.task.token)

class StartSubProcess(mixins.TaskDescriptionMixin,
                      mixins.NextNodeMixin,
                      mixins.DetailViewMixin,
                      mixins.UndoViewMixin,
                      mixins.CancelViewMixin,
                      mixins.PerformViewMixin,
                      Event):
                 
    """
        start = StartSubProcess().Next(this.other_node)
        other_node = flow.View().Next(this.end)
        end = flow.End()
    """
    task_type = 'STARTSUBPROCESS'
    activation_class = StartSubProcessActivaton

    cancel_view_class = views.CancelTaskView
    detail_view_class = views.DetailTaskView
    perform_view_class = views.PerformTaskView
    undo_view_class = views.UndoTaskView

    def __init__(self,start_func=None, **kwargs):

        self.func = start_func if start_func is not None else self.start_func_default
        super(StartSubProcess, self).__init__(**kwargs)

    @method_decorator(flow_start_func)
    def start_func_default(self, activation, *args):
        """ Start a new process and record parent info """
        self.parent_process = args[0]
        self.parent_task = args[1]
        activation.prepare(self.parent_process, self.parent_task)
        activation.done()
        return activation

    def start(self, parent_process, parent_task, *args, **kwargs):
       """ run fun initilize activation"""
       return self.func(self, parent_process, parent_task, *args, **kwargs)

    def ready(self):
        """
           Resolbe this relationship 
        """
        if isinstance(self.func, ThisObject):
            self.func = getattr(self.flow_class.instance, self.func.name)
