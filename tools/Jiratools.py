# -*-coding:utf-8 -*-
import os
from jira import JIRA
from tools.Logger import logs

logger = logs('JiraTool.py').getLogger()  # 调用logger接口


class JiraTool:
    def __init__(self, username, password, project=None):
        self.server = 'https://hyper-optic.atlassian.net'
        self.username = username
        self.password = password
        self.project = project
        self.jira_conn = JIRA(server=self.server, basic_auth=(self.username, self.password))  # jira服务器，用户名密码

    def get_projects(self):
        """访问权限的项目列表:[<JIRA Project: key='AR2022011', name='识别', id='12882'>,...]"""
        # for p in self.jira_conn.projects():
        #     print(p.key, p.id, p.name)
        return self.jira_conn.projects()

    def get_project(self, project_id):
        """
        通过项目id/key获取项目主要属性：
        key: 项目的Key
        name: 项目名称
        description: 项目描述
        lead: 项目负责人
        projectCategory: 项目分类
        components: 项目组件
        versions: 项目中的版本
        raw: 项目的原始API数据
        """
        project = {
            'key': self.jira_conn.project(project_id).key,
            'name': self.jira_conn.project(project_id).name,
            'description': self.jira_conn.project(project_id).description,
            'lead': self.jira_conn.project(project_id).lead,
            'components': self.jira_conn.project(project_id).components,
            'versions': self.jira_conn.project(project_id).versions,
            'raw': self.jira_conn.project(project_id).raw
        }
        return project

    def search_jira_jql(self, jql=None, maxnum: int = None):
        """根据jql查询jira,返回[<JIRA Issue: key='PJT-9141', id='302682'>,...]"""
        maxResults = False if maxnum is None else maxnum
        issues = self.jira_conn.search_issues(jql, maxResults=maxResults, json_result=False)
        return issues

    def create_issue(self, issue_dict):
        """
        创建issue,issue_dict = {
        'project': {'id': 10000},
        'summary': 'BUG描述',
        'description': 'BUG详情 \n换行',
        'priority': {'name': 'BUG优先级'},
        'labels': ['标签'],
        'issuetype': {'name': '问题类型-故障'},
        'assignee':{'name': '经办人'} #经办人
        }
        """
        self.jira_conn.create_issue(fields=issue_dict)

    def create_issues(self, issue_list):
        """
        批量创建issue,issue_list = [issue_dict1, issue_dict2, issue_dict3]
        """
        self.jira_conn.create_issues(issue_list)

    def get_issue(self, issue_id):
        """获取issue信息"""
        issue = self.jira_conn.issue(issue_id)
        return issue

    def get_fewfields(self, issue_id):
        fewfields = self.get_issue(issue_id).fields
        fields = {
            'Time_to_response_WCT': fewfields.customfield_12203,
            'OSS_Service_Request_Response': fewfields.customfield_16091,
            'assignee': fewfields.assignee,
            'comment': fewfields.comment.comments,
            'issuetype': fewfields.issuetype
        }
        return fields


    def get_issueType(self, issue_id):
        """获取issue-type信息:"""
        issuefields = self.get_issue(issue_id).fields
        return issuefields.issuetype

    def get_issuefields(self, issue_id):
        """获取issue-fields信息:"""
        issuefields = self.get_issue(issue_id).fields
        fields = {
            'summary': issuefields.summary,
            'assignee': issuefields.assignee,
            'status': issuefields.status,
            'issuetype': issuefields.issuetype,
            'reporter': issuefields.reporter,
            'labels': issuefields.labels,
            'priority': issuefields.priority.name,
            'description': issuefields.description,
            'created': issuefields.created,
            'versions': issuefields.versions,
            'fixVersions': issuefields.fixVersions
        }
        return fields

    def get_summary(self, issue_id):
        """获取issue-summary信息:"""
        issuefields = self.get_issue(issue_id).fields
        return issuefields.summary

    def get_issuelabels(self, issue_id):
        """获取issue-issuelabels信息:"""
        issuefields = self.get_issue(issue_id).fields
        labels = issuefields.labels
        return labels

    def get_status(self, issue_id):
        """查询状态"""
        return self.jira_conn.issue(issue_id).fields.status

    def get_assignee(self, issue_id):
        """查询assignee"""
        return self.jira_conn.issue(issue_id).fields.assignee
        # return self.jira_conn.issue(issue_id).assignee

    def find_description(self, issue_id):
        """查询description信息"""
        return self.jira_conn.issue(issue_id).fields.description

    def update_issue(self, issue_id, issue_dict):
        """
        创建issue,issue_dict = {
        'project': {'id': 10000},
        'summary': 'BUG描述',
        'description': 'BUG详情 \n换行',
        'priority': {'name': 'BUG优先级'},
        'labels': ['标签'],
        'issuetype': {'name': '问题类型-故障'},
        'assignee':{'name': '经办人'} #经办人
        }
        update(assignee={'name': username})
        """
        self.jira_conn.issue(issue_id).update(issue_dict)

    def get_versions(self, jira_key):  # 获取Jira影响版本
        versions = [v.name for v in self.jira_conn.issue(jira_key).fields.versions]
        return versions

    def add_version(self, jira_key, versions_name):  # 为Jira添加影响版本,注意新增的版本在JIRA中是否存在,否则报错
        self.jira_conn.issue(jira_key).add_field_value('versions', {'name': versions_name})

    def del_version(self, jira_key, versions_name):  # 获取Jira影响版本
        oldversions = [i.name for i in self.jira_conn.issue(jira_key).fields.versions]
        newversions = oldversions
        if versions_name in oldversions:
            oldversions.remove(versions_name)
            newversions = oldversions
        versions = [{'name': f} for f in newversions]
        self.jira_conn.issue(jira_key).update(fields={'versions': versions})

    def get_fixversions(self, jira_key):  # 获取Jira影响版本
        fixVersions = [v.name for v in self.jira_conn.issue(jira_key).fields.fixVersions]
        return fixVersions

    def add_fixversions(self, jira_key, fixversions_name):  # 为Jira添加解决版本,注意新增的版本在JIRA中是否存在,否则报错
        self.jira_conn.issue(jira_key).add_field_value('fixVersions', {'name': fixversions_name})

    def del_fixversions(self, jira_key, versions_name):  # 获取Jira影响版本
        oldfixversions = [i.name for i in self.jira_conn.issue(jira_key).fields.fixVersions]
        newfixversions = oldfixversions
        if versions_name in oldfixversions:
            newfixversions.remove(versions_name)
            newfixversions = oldfixversions
        versions = [{'name': f} for f in newfixversions]
        self.jira_conn.issue(jira_key).update(fields={'fixVersions': versions})

    def add_field_value(self, issue_id, key, value):
        issue = self.jira_conn.issue(issue_id)
        issue.add_field_value(field=key, value=value)

    def add_attachment(self, jira_key, picpath):
        """上传附件"""
        issue = self.jira_conn.issue(jira_key)
        with open(picpath, 'rb') as f:
            self.jira_conn.add_attachment(issue, attachment=f)
        f.close()

    def get_comments(self, issue_id):
        """查询comments"""
        comments = self.jira_conn.issue(issue_id).fields.comment.comments
        # return { comment.id:comment.author for comment in comments}
        # return { comment.id:comment.body for comment in comments}
        return comments

    def add_comment(self, jira_key, context, picpath=None):
        """添加comment"""
        if picpath is None or not os.path.exists(picpath):
            comment = context
        else:
            self.add_attachment(jira_key, picpath)
            picname = os.path.basename(picpath)
            comment = f"{context}\r\n!{picname}|thumbnail!"
        self.jira_conn.add_comment(jira_key, comment)

    def update_comment(self, issue_id, comment_id, n_comment):
        """更新comment"""
        issue = self.jira_conn.issue(issue_id)
        comment = self.jira_conn.comment(issue, comment_id)
        comment.update(body=n_comment)

    def get_transitions(self, issue_id):
        """查询当前权限下问题流程可操作节点"""
        issue = self.jira_conn.issue(issue_id)
        transitions = self.jira_conn.transitions(issue)
        return [(t['id'], t['name']) for t in transitions]

    def update_status(self, issue_id=None, status=None, **kwargs):
        """更新问题流程状态"""
        issue = self.jira_conn.issue(issue_id)
        self.jira_conn.transition_issue(issue, status, **kwargs)

    def close_client(self):  # 关闭链接
        self.jira_conn.close()

    @staticmethod
    def get_id_by_name(self, name: str):
        user_id_dict = {
            'Chen Zheng': '6143711de057c6006a479c1c',
            'Alam MdKourshed': '63282b8b409249995ee611a8',
            'Zhu Ganghua': '614374f1e057c6006a47c6ff',
            'MalindaAnupama.Malavisooriya': '61f0c6bf5a0988006b362495',
            'he.tianchang': '6177c08f062f4c0069a0aca8',
            'Wang Wei': '61437199805a97006ac5a781',
            'Cai Haozhe': '617344363e3753006fc5beb3'
        }
        # 判断name是否在list中
        if name in user_id_dict.keys():
            # 返回结果
            return user_id_dict[name]
        else:
            return 'name_not_exist'

    def jira_response_scan(self, issueKeyList):
        """
        desc: check the open issue response status.
        :param issueKeyList: the jira ticket number list
        :return: no return
        """

        for issue in issueKeyList:
            issuekey = issue.key
            # 获取comment
            issueComments = self.get_comments(issuekey)
            if len(issueComments) == 0:
                # 如果comments长度是0，代表还没有回复，则需要回复，这个是service request单，直接执行就可以了
                logger.warning('[%s] comment长度为0，需要添加comment' % issuekey)
                assignee1 = self.get_assignee(issuekey)
                str_assignee_id = self.get_id_by_name(str(assignee1))
                if str_assignee_id != 'name_not_exist':
                    self.add_comment(issuekey, 'Hi [~accountid:%s] please process asap, thanks' % str_assignee_id)
                else:
                    self.add_comment(issuekey, 'Hi %s please process asap, thanks' % str(assignee1))
                logger.info('[%s] 已完成添加comment' % issuekey)
            elif len(issueComments) == 1:
                # 如果comments长度是1， 则需要查看comment的作者是谁，如果是Admin，则需要回复
                # 获取comment作者
                commentAuthor = {comment.id: comment.author for comment in issueComments}
                commentID = list({comment.id for comment in issueComments})

                if str(commentAuthor[commentID[0]]) == 'Admin':
                    # 这个是incident单，需要排查问题
                    logger.warning('[%s] comment长度为1，但是Reporter是Admin，需要添加comment' % issuekey)
                    assignee1 = self.get_assignee(issuekey)
                    # self.add_comment(issuekey, 'has pushed to %s, will check it asap, thanks' % assignee)
                    str_assignee_id = self.get_id_by_name(str(assignee1))
                    if str_assignee_id != 'name_not_exist':
                        self.add_comment(issuekey, 'Hi [~accountid:%s] please check asap, thanks' % str_assignee_id)
                    else:
                        self.add_comment(issuekey, 'Hi %s please check asap, thanks' % str(assignee1))

                    logger.info('[%s] 已完成添加comment' % issuekey)
                else:
                    logger.info(
                        '[%s] comment作者是[%s]，已经回复，不需要添加comment' % (issuekey, commentAuthor[commentID[0]]))
            else:
                logger.info('[%s] comment长度大于1，已经回复，不需要添加comment' % issuekey)

    def get_jira_sla(self, issueKey):
        """
        DESC: get jira SLA info, and send notification by email.
        :param issueKey:the jira ticket number
        :return:
        """

        pass

    def get_title(self, issueKey):
        return self.get_issue(issueKey).fields.summary


if __name__ == '__main__':
    jiratool = JiraTool(username='xu.xinkai2@iwhalecloud.com',
                        password='ATATT3xFfGF0ObxKYcUD9R4R7kfSSjILK8H3oIczMatM2c5BPZRxgDnRggDKvuPUnMxxsHRT28ammKCBR2Eg6rjSs1Xpm0lVwFDbyO3pPBS_KHNfNQNfTY3gH0h28WHdUwroeIBrLLQ2sjpi7OM0Bdu2ay0zHTZMROWmhuckgCFdr82bDY1KCkk=3CC37AEF')

    issueKeys = list([
'SS-52465',
'SS-52516'])

    for key in issueKeys:
        print('%s,%s,%s' % (key, jiratool.get_issue(key).fields.created, jiratool.get_issue(key).fields.summary))

    jiratool.close_client()
