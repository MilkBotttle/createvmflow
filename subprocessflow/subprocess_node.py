from viewflow.activation import * 
from viewflow import mixins, Event, ThisObject
from django.utils.decorators import method_decorator
from viewflow.decorators import flow_start_func
from viewflow.flow import views
# Subprocess    
class SubProcessActivation(Activation):
    """Inhir funcactivation"""
    def prep_subprocess(self):
        self._subflow = self.flow_task.subflow

    @Activation.status.transition(source=STATUS.NEW)
    def perform(self):
        """Perform the subprocess"""

        self.task.started = now()

        signals.task_started.send(
            sender=self.flow_class,
            process=self.process,
            task=self.task)
        #run subprocess activate
        self._subflow.start(self.process, self.task)
        #sub_activation = self._subflow.start(self.parent_process)
 
#        self.set_status(STATUS.DONE)
#        self.task.save()
#
#        signals.task_finished.send(
#            sender=self.flow_class,
#            process=self.process,
#            task=self.task)

#        self.activate_next()
            
    def activate_next(self):
        """Activate all outgoing edges."""
        self.set_status(STATUS.DONE)
        self.task.save()

        signals.task_finished.send(
            sender=self.flow_class,
            process=self.process,
            task=self.task)
        if self.flow_task._next:
            self.flow_task._next.activate(
                prev_activation=self, token=self.task.token)

    @classmethod
    def activate(cls, flow_task, prev_activation, token):
        task = flow_task.flow_class.task_class(
            process=prev_activation.process,
            flow_task=flow_task,
            token=token)
        task.save()
        task.previous.add(prev_activation.task)

        activation = cls()
        activation.initialize(flow_task, task)
        activation.prep_subprocess()
        activation.perform()

        return activation

    def is_done(self):
        subprocess_class = self.flow_task.subflow.flow_class.process_class
        subprocesses = subprocess_class._default_manager.filter(parent_task=self.task).exclude(status=STATUS.DONE).exists()
        return not subprocesses

class SubProcess(mixins.TaskDescriptionMixin,
                 mixins.NextNodeMixin,
                 mixins.DetailViewMixin,
                 mixins.UndoViewMixin,
                 mixins.CancelViewMixin,
                 mixins.PerformViewMixin,
                 Event):
    """
        start_sub = (
            SubProcess(sub_flow)
                .Next(this.end)
        )
    """
    task_type = 'SUBPROCESS'
    activation_class = SubProcessActivation
    
    cancel_view_class = views.CancelTaskView
    detail_view_class = views.DetailTaskView
    perform_view_class = views.PerformTaskView
    undo_view_class = views.UndoTaskView

    def __init__(self, subflow, **kwargs):
        self.subflow = subflow        
        super(SubProcess, self).__init__(**kwargs)

    def on_subprocess_end(self, **signal_kwargs):
        process = signal_kwargs['process']                  
                                                            
        if process.parent_task:                             
            activation = self.activation_class()              
            activation.initialize(self, process.parent_task)
            if activation.is_done():
                activation.activate_next()                           
    
    def ready(self, **singnal_args):
        signals.flow_finished.connect(self.on_subprocess_end, sender=self.subflow.flow_class) 

class StartSubProcessActivaton(StartActivation):
    """ Start a new subprocess """
    @Activation.status.transition(source=STATUS.NEW, target=STATUS.PREPARED)
    def prepare(self,parent_process,parent_task):
        if self.task.started is None:
            self.task.started = now()
        self.process.parent_process = parent_process
        self.process.parent_task = parent_task

    def activate_next(self):
        if self.flow_task._next:
            self.flow_task._next.activate(
                prev_activation=self, token=self.task.token)        

    @Activation.status.super()
    def initialize(self, flow_task, task):
        """ Initialize an activation. """
        self.lock = None 
        self.flow_task, self.flow_class = flow_task, flow_task.flow_class

        self.process = self.flow_class.process_class(
            flow_class=self.flow_class)  
        self.task = self.flow_class.task_class(flow_task=self.flow_task)        
        

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
        self.parent_process = args[0]
        self.parent_task = args[1]
        activation.prepare(self.parent_process, self.parent_task)
        activation.done()
        return activation

    def on_flow_finished(self, **signal_kwargs):
        process = signal_kwargs['process']

        if process.parent_task:
            activation = self.activation_cls()
            activation.initialize(self, process.parent_task)
            if activation.is_done():
                activation.done()

    def start(self, parent_process, parent_task, *args, **kwargs):
       """ run fun initilize activation"""
       return self.func(self, parent_process, parent_task, *args, **kwargs)

    def ready(self):
        if isinstance(self.func, ThisObject):
            self.func = getattr(self.flow_class.instance, self.func.name)
