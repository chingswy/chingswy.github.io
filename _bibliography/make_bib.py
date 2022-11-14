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
from glob import glob
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
    record['year'] = int(year)
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
    for key in ['Qing', 'Sida', 'code', 'preview']:
        if key in value.keys():
            record[key] = value[key]
    if 'author' not in value.keys() and 'author' not in record.keys():
        record['author'] = []
    assert 'title' in record.keys(), value
    return record

def reading_yml(filename, default_config):
    if os.path.exists(global_cache_name):
        with open(global_cache_name, 'r') as f:
            global_cache = yaml.safe_load(f)
    else:
        global_cache = {}
    with open(filename, 'r') as f:
        datas = yaml.safe_load(f)
    records = []
    for key, value in datas.items():
        if not isinstance(key, str):
            key = str(key)
        if key in global_cache.keys():
            record = global_cache[key]
            records.append(record)
            continue
        record = {
            'key': key
        }
        # 替换一下value的键名
        for alias_name, key_name in [('Q', 'Qing'), ('k', 'keywords'), ('t', 'title')]:
            if alias_name in value.keys() and key_name not in value.keys():
                value[key_name] = value.pop(alias_name)
        if 'url' in value.keys() and 'arxiv' in value['url']:
            record = parsing_arxiv_paper(value, record)
        elif 'url' in value.keys():
            record['html'] = value['url']
        for default_key, default_value in default_config.items():
            if default_key not in record.keys():
                record[default_key] = default_value
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
        # 看看有没有图片
        imgnames = glob(join('assets', 'paper-reading', record['key']+'*'))
        if len(imgnames) == 1:
            record['preview'] = imgnames[0]
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
        for key in ['booktitle', 'journal', 'html', 'code', 'preview', 'Qing', 'abstract', 'Sida']:
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
            '_bibliography/mv1p.yml': {'category': 'human'},
            '_bibliography/arxiv2210.yml': {},
            '_bibliography/eccv22_human.yml': {
                'category': 'human',
                'year': 2022,
                'booktitle': 'ECCV',
            },
        },
        'output_sida.bib': {
            '_bibliography/sida.yml': {}
        },
        'eccv22_human.bib':{
            '_bibliography/eccv22_human.yml': {
                'year': 2022,
                'category': 'human',
                'booktitle': 'ECCV',
            },
        }
    }
    tags_all, years_all = [], []
    for outname, configs in config.items():
        records = []
        for filename, default_config in configs.items():
            records.extend(reading_yml(filename, default_config))
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
