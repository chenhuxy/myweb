#!/usr/bin/env python
#coding:utf-8

"""
gitlab 经常使用到的api
DOC_URL: http://python-gitlab.readthedocs.io/en/stable/
LOCAL_PATH: C:\Python36\Lib\site-packages\gitlab
"""

import gitlab
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponse
import json
import pickle


class GitTools:
    def __init__(self,git_url,git_token):
        self.git_url = git_url
        self.git_token = git_token

    def projects(self):
        gl=gitlab.Gitlab(self.git_url,self.git_token)
        #projects1 = gl.projects.list()
        projects = gl.projects.list(all=True,as_list=False)
        #for p in gl.projects.list(all=True, as_list=False):
        #    print(p.name, p.id)
        #for p in gl.projects.list(page=1):
        #    print(p.name, p.id)
        #project = gl.projects.get('proj')
        #project2 = gl.projects.list(search='kw', visibility='public')
        #project3 = gl.projects.create({'name': 'proj'})
        res = {}
        for p in projects:
            #print(p.id,p.name,p.http_url_to_repo)
            return {'id':p.id,'name':p.name,'repo':p.http_url_to_repo}

        #return projects

    '''
    def projects(self):
        dic = {}
        gl = gitlab.Gitlab(self.git_url, self.git_token)
        for g in gl.groups.list(all=True):
            for p in g.projects.list(all=True):
                print("group: %s, project,id: %s,%s" % (g.name, p.name, p.id))
                project = gl.projects.get(p.id)
                branches = []
                for b in project.branches.list():
                    branches.append(b.name)
                print("project branches: ", branches)
                k = str(g.name) + '/' + str(p.name)
                if k not in dic:
                    dic[k] = branches
        return dic
        '''


    def get_branches(self,project):
        branches = project.branches.list()
        #branch = project.branches.get('branch')
        #branch2 = project.branches.create({'branch_name': 'branch',
        #                                   'ref': 'master'})
        #project.branches.delete('branch')
        #branch.protect()
        #branch.unprotect()
        return branches

    def tags(self,project):
        tags = project.tags.list(all=True)
        tags = project.tags.list('1.0')
        tag = project.tags.create({'tag_name': '1.0', 'ref': 'master'})
        tag.set_release_description('awesome v1.0 release')
        project.tags.delete('1.0')
        tag.delete()

    def commits(self,project):
        commits = project.commits.list()
        for c in commits:
            print(c.author_name, c.message, c.title)
        commit = project.commits.get('e3d5a71b')

    def mrs(self,project):
        mrs = project.mergerequests.list()
        print(mrs)
        mr = project.mergerequests.get('mr_id')
        mr = project.mergerequests.create({'source_branch': 'cool_feature',
                                           'target_branch': 'master',
                                           'title': 'merge cool feature', })
        mr.description = 'New description'
        mr.save()
        mr.state_event = 'close'  # or 'reopen'
        mr.save()
        project.mergerequests.delete('mr_id')
        mr.delete()
        mr.merge()
        mrs = project.mergerequests.list(state='merged', sort='asc')  # all, merged, opened or closed

    def do_commit(self,project):
        data = {
            'branch_name': 'master',  # v3
            'commit_message': 'blah blah blah',
            'actions': [
                {
                    'action': 'create',
                    'file_path': 'blah',
                    'content': 'blah'
                }
            ]
        }
        commit = project.commits.create(data)

        result = project.repository_compare('develop', 'feature-20180104')
        print(result)

        for commit in result['commits']:
            print(commit)

        for file_diff in result['diffs']:
            print(file_diff)

        for commit in result['commits']:
            print(commit)

        for file_diff in result['diffs']:
            print(file_diff)




def git_project(request,*args,**kwargs):
    git_url = 'http://10.180.11.8'
    git_token = 'F7nAGXozy4dsfJvxiLu_'
    git_tools = GitTools(git_url,git_token)
    msg=git_tools.projects()
    print(msg,type(msg))
    return render_to_response('monitor/gitlab.html',msg)
    #return HttpResponse(msg)


