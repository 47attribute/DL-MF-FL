import requests
import json
from bs4 import BeautifulSoup
from xml.dom import minidom


def generateXML(pid, version, summary, description, modified):
    dom = minidom.Document()
    root_node = dom.createElement('bugrepository')
    root_node.setAttribute('name', pid)
    dom.appendChild(root_node)

    bug_node = dom.createElement('bug')
    root_node.appendChild(bug_node)
    bug_node.setAttribute('id', version)
    bug_node.setAttribute('opendate', '')
    bug_node.setAttribute('fixdate', '')

    info_node = dom.createElement('buginformation')
    fix_node = dom.createElement('fixedFiles')
    bug_node.appendChild(info_node)
    bug_node.appendChild(fix_node)

    summary_node = dom.createElement("summary")
    info_node.appendChild(summary_node)
    summary_text = dom.createTextNode(summary)
    summary_node.appendChild(summary_text)

    desc_node = dom.createElement("description")
    info_node.appendChild(desc_node)
    desc_text = dom.createTextNode(description)
    desc_node.appendChild(desc_text)

    for i in modified:
        file_node = dom.createElement("file")
        fix_node.appendChild(file_node)
        file_text = dom.createTextNode(i + ".java")
        file_node.appendChild(file_text)

    try:
        with open("XMLfile/" + pid + "/" + version + '.xml', 'w', encoding='UTF-8') as fh:
            dom.writexml(fh, indent='', addindent='\t', newl='\n', encoding='UTF-8')
            print(pid + '-' + version + ' 写入XML成功!')
    except Exception as err:
        print('错误信息：{0}'.format(err))


 for pid in ['Chart', 'Cli', 'Closure', 'Codec', 'Collections', 'Compress', 'Csv', 'Gson', 'JacksonCore',
            'JacksonDatabind', 'JacksonXML', 'Jsoup', 'JxPath', 'Lang', 'Math', 'Mockito', 'Time']:

    # Jsoup 45 url无效

    with open('Data/' + pid, 'r') as lines:
        for line in lines:
            version = line.split(',')[0]
            bid = line.split(',')[1]
            if bid == 'UNKNOWN': continue
            url = line.split(',')[2]
            modified = line.split(',')[3].replace('\"', '').replace('\n', '').split(';')

            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')

            # D4J 2.0.0 四类url获取 summary 和 description
            if 'sourceforge.net' in url:
                summary = soup.h2.text.replace('\n', '').strip()
                description = soup.find('div', class_='markdown_content').text.replace('\n', ' ').replace('\r', '')
            elif 'issues.apache.org' in url:
                summary = soup.find('h1', id='summary-val').text
                # description 缺失
                try:
                    description = soup.find('div', class_='user-content-block').text.replace('\n', ' ').replace('\r', '')
                except:
                    description = ''
            elif 'github.com' in url:
                summary = soup.find('h1', class_='gh-header-title mb-2 lh-condensed f1 mr-0 flex-auto break-word') \
                    .text.replace('\n', '').strip()
                description = soup.find('div', class_='edit-comment-hide').text.replace('\n', ' ').strip()
            elif 'storage.googleapis.com' in url:
                d = json.loads(r.text)
                summary = d['summary']
                description = d['comments'][0]['content'].replace('\n', '').replace('\r', '')

            generateXML(pid, version, summary, description, modified)
