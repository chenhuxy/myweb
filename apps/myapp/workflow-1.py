#!/usr/bin/env python
#coding:utf-8

from __future__ import print_function
from SpiffWorkflow.specs import WorkflowSpec, ExclusiveChoice, Simple, Cancel
from SpiffWorkflow.operators import Equal, Attrib
from django.shortcuts import render_to_response
from apps.myapp import views
from apps.myapp import tasks
from apps.myapp import models

def my_nuclear_strike(msg):
    print("Launched:", msg)



class NuclearStrikeWorkflowSpec(WorkflowSpec):
    def __init__(self):
        WorkflowSpec.__init__(self)

        # The first step of our workflow is to let the general confirm
        # the nuclear strike.
        general_choice = ExclusiveChoice(self, 'general')
        #general_choice = ExclusiveChoice(self, tasks.send_mail())
        self.start.connect(general_choice)

        # The default choice of the general is to abort.
        cancel = Cancel(self, 'workflow_aborted')
        general_choice.connect(cancel)

        # Otherwise, we will ask the president to confirm.
        president_choice = ExclusiveChoice(self, 'president')
        cond = Equal(Attrib('confirmation'), 'yes')
        general_choice.connect_if(cond, president_choice)

        # The default choice of the president is to abort.
        president_choice.connect(cancel)

        # Otherwise, we will perform the nuclear strike.
        strike = Simple(self, 'nuclear_strike')
        president_choice.connect_if(cond, strike)

        # Now we connect our Python function to the Task named 'nuclear_strike'
        strike.completed_event.connect(my_nuclear_strike)
        #strike.completed_event.connect(views.wf)

        # As soon as all tasks are either "completed" or  "aborted", the
        # workflow implicitely ends.
'''
if __name__=="__main__":
    my_nuclear_strike('hello,workflow')
'''