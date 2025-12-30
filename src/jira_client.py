from jira import JIRA

def test_jira_connection(url, email, token, project_key):
    try:
        jira = JIRA(server=url, basic_auth=(email, token))
        myself = jira.myself()
        project = jira.project(project_key)
        valid_types = [t.name for t in project.issueTypes]
        return True, f"✅ Bağlantı Başarılı! Kullanıcı: {myself['displayName']}", valid_types
    except Exception as e:
        error_msg = str(e)
        if hasattr(e, 'response'):
            error_msg += f" (HTTP {e.response.status_code})"
        return False, f"❌ Bağlantı Hatası: {error_msg}", []

def create_jira_issue(config, issue_data):
    
    try:
        jira = JIRA(server=config['url'], basic_auth=(config['user'], config['token']))
        
        issue_dict = {
            'project': {'key': config['project']},
            'summary': issue_data['summary'],
            'description': issue_data['description'],
            'issuetype': {'name': config['issuetype']},
            'priority': {'name': issue_data['priority']}
        }
        
        new_issue = jira.create_issue(fields=issue_dict)
        return True, new_issue.key
    except Exception as e:
        err_msg = str(e)
        if hasattr(e, 'response'):
             err_msg += f" | Server: {e.response.text}"
        return False, f"Oluşturma Hatası: {err_msg}"