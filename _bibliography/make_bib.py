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
from os.path import join
import os
dirname = os.path.abspath(os.path.dirname(__file__))

mywarn = print
log = print
def run_cmd(cmd):
    os.system(cmd)

def check_exists(path, min_l=1):
    flag1 = os.path.isfile(path) and os.path.exists(path)
    flag2 = os.path.isdir(path) and len(os.listdir(path)) >= min_l
    if not flag1 and not flag2:
        mywarn('[Check] {} not exists'.format(path))
    return flag1 or flag2

def mkdir(path, verbose=True):
    if not os.path.exists(path):
        log('mkdir {}'.format(path))
        os.makedirs(path, exist_ok=True)

def parsing_arxiv_paper(value, record):
    url = value['url']
    record['html'] = url
    arxivid = url.split('/')[-1].replace('.pdf', '')
    year = '20' + arxivid[:2]
    record['year'] = year
    print('>> searching paper {} in arxiv'.format(url))
    search = arxiv.Search(id_list=[arxivid])
    results = list(search.results())
    assert len(results) == 1, url
    result = results[0]
    record['title'] = result.title
    record['author'] = [d.name for d in result.authors]
    record['abstract'] = result.summary.replace('\n', '')
    # 爬取figure
    if 'figure' in value.keys():
        tarname = join(dirname, '_arxiv', f'{arxivid}.tar.gz')
        mkdir(os.path.dirname(tarname))
        if not check_exists(tarname):
            cmd = 'curl https://arxiv.org/e-print/{} --output {}'.format(arxivid, tarname)
            run_cmd(cmd)
        sourcename = join(dirname, '_arxiv', arxivid)
        if not check_exists(sourcename):
            mkdir(sourcename, verbose=False)
            cmd = f'tar -xzf {tarname} -C {sourcename}'
            run_cmd(cmd)
    return record

def parsing_my_info(value, record):
    if 'title' in value.keys() and 'title' not in record.keys():
        record['title'] = value['title']
    if 'keywords' in value.keys():
        keywords = value['keywords'].split(', ')
        for i, keyword in enumerate(keywords):
            keywords[i] = keyword.replace(' ', '-')
        record['tags'] = keywords
    for key in ['Qing', 'Sida', 'code']:
        if key in value.keys():
            record[key] = value[key]
    assert 'title' in record.keys(), value
    return record

def reading_yml(filename, category):
    if os.path.exists(global_cache_name):
        with open(global_cache_name, 'r') as f:
            global_cache = yaml.safe_load(f)
    else:
        global_cache = {}
    with open(filename, 'r') as f:
        datas = yaml.safe_load(f)
    records = []
    for key, value in datas.items():
        if key in global_cache.keys():
            record = global_cache[key]
            records.append(record)
            continue
        record = {
            'key': key
        }
        if 'url' in value.keys() and 'arxiv' in value['url']:
            record = parsing_arxiv_paper(value, record)
        record = parsing_my_info(value, record)
        global_cache[key] = record
        records.append(record)
    with open(global_cache_name, 'w') as f:
        yaml.safe_dump(global_cache, f, allow_unicode=True)
    return records

def write_to_bib(records, outname):
    outputs = ['---', '---']
    years, tags = set(), set()
    for record in records:
        res = '@inproceedings{{{},'.format(record['key'])
        outputs.append(res)
        outputs.append('  title={{{}}},'.format(record['title']))
        if 'author' in record.keys():
            outputs.append('  author={{{}}},'.format(' and '.join(record['author'])))
        if 'year' in record.keys():
            outputs.append('  year={{{}}},'.format(record['year']))
            years.add(record['year'])
        if 'tags' in record.keys():
            outputs.append('  tags={{{}}},'.format(', '.join(record['tags'])))
            tags = tags | set(record['tags'])
        for key in ['html', 'code', 'Qing', 'abstract', 'Sida']:
            if key in record.keys():
                outputs.append('  {}={{{}}},'.format(key.lower(), record[key]))
        outputs.append('  bibtex_show={{true}},'.format())
        outputs.append('}')
        outputs.append('')
    print('\r\n'.join(outputs), file=open(outname, 'w'))
    years = sorted(list(years))[::-1]
    tags = sorted(list(tags))
    return years, tags

if __name__ == '__main__':
    global_cache_name = join(dirname, '_global_cache.yml')
    config = {
        'output.bib': {
            '_bibliography/mv1p.yml': 'human',
            '_bibliography/arxiv2210.yml': 'none'
        },
        'output_sida.bib': {
            '_bibliography/sida.yml': 'none'
        }
    }
    tags_all, years_all = [], []
    for outname, configs in config.items():
        records = []
        for filename, category in configs.items():
            records.extend(reading_yml(filename, category))
        years, tags = write_to_bib(records, outname = join(dirname, outname))
        tags_all.extend(tags)
        years_all.extend(years)
    years_all = set(years_all)
    tags_all = set(tags_all)
    years = sorted(list(years_all))[::-1]
    tags = sorted(list(tags_all))
    with open(join(dirname, '..', '_data', 'reading.yml'), 'w') as f:
        yaml.safe_dump({
            'years': years,
            'tags': tags,
        }, f, allow_unicode=True)
