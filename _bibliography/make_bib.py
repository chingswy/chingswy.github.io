'''
  @ Date: 2022-11-07 16:01:43
  @ Author: Qing Shuai
  @ Mail: s_q@zju.edu.cn
  @ LastEditors: Qing Shuai
  @ LastEditTime: 2022-11-07 16:49:56
  @ FilePath: /chingswy.github.io/_bibliography/make_bib.py
'''
import yaml
import arxiv

with open('arxiv2210.yml', 'r') as f:
    datas = yaml.safe_load(f)

outname = 'output.bib'

outputs = ['---', '---']

for key, value in datas.items():
    data = {}
    assert 'url' in value.keys(), key
    url = value['url']
    if 'arxiv' in url:
        html = url
        arxivid = url.split('/')[-1].replace('.pdf', '')
        year = '20' + arxivid[:2]
        print('>> searching paper {} in arxiv'.format(key))
        search = arxiv.Search(id_list=[arxivid])
        results = list(search.results())
        assert len(results) == 1, url
        result = results[0]
        data['title'] = result.title
        data['author'] = ' and '.join([d.name for d in result.authors])
    else:
        html = None
    if 'keywords' in value.keys():
        keywords = value['keywords'].split(', ')
        data['tags'] = ', '.join(keywords)
    res = '@inproceedings{{{},'.format(key)
    outputs.append(res)
    outputs.append('  title={{{}}},'.format(data['title']))
    outputs.append('  author={{{}}},'.format(data['author']))
    outputs.append('  year={{{}}},'.format(year))
    if 'tags' in data.keys():
        outputs.append('  tags={{{}}},'.format(data['tags']))
    if html is not None:
        outputs.append('  html={{{}}},'.format(html))
    outputs.append('  bibtex_show={{true}},'.format())
    outputs.append('}')
    outputs.append('')

print('\r\n'.join(outputs), file=open(outname, 'w'))