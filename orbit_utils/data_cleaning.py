import pandas as pd
import re

def remove_likely_table_blocks(text):
    pattern = re.compile(r'arXiv:[^\s]+(?:v\d+)?\s+')
    lines = text.split('\n')
    new_lines = []
    skip = False
    for line in lines:
        if 'table' in line.lower() or line.strip().startswith(('ID', 'α', 'δ')):
            skip = True
        if skip and line.strip() == '':
            skip = False
            continue
        if not skip:
            new_lines.append(line)

    text = '\n'.join(new_lines)
    text = pattern.sub('', text)
    return text


def remove_number_only_lines(text):
    lines = text.split('\n')
    cleaned_lines = []
    pattern = re.compile(r'^(\d+([.,]\d+)?(-\d+([.,]\d+)?)?(\s+(\d+([.,]\d+)?(-\d+([.,]\d+)?)?))*)$')

    for line in lines:
        line_strip = line.strip()
        if not pattern.match(line_strip):
            cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)


def extract_inner_args(col_list, col_name):
    if isinstance(col_list, list):
        return [c.get(col_name) for c in col_list if col_name in c]
    else:
        return []


def extract_landing_page(col_dict):
    return col_dict.get('landing_page_url') if isinstance(col_dict, dict) else None

    
def expand_dict_columns(df, col_name, drop_original=True):
    """
    Nimmt ein DataFrame df und eine Spalte col_name mit dicts,
    wandelt den Inhalt in separate Spalten um.
    Gibt das erweiterte DataFrame zurück.
    """
    # 1. neue DataFrame mit allen Dict-Feldern
    dict_df = pd.DataFrame(df[col_name].tolist(), index=df.index)
    
    # 2. hänge neue Spalten an
    df_expanded = pd.concat([df, dict_df], axis=1)
    
    # 3. optional: Original-Spalte entfernen
    if drop_original:
        df_expanded = df_expanded.drop(columns=[col_name])
    
    return df_expanded


def clean_cols(data, file_path):
    data = data.drop(columns=['link'])
    data = data.drop(columns=['authors'])
    data = data.drop(columns=['category'])
    data = data.drop(columns=['host_venue'])
    data = data.drop(columns=['host_venue_license'])
    data = data.drop(columns=['mesh'])
    data = data.drop(columns=['grants'])
    data = data.drop(columns=['is_paratext'])

    data['full_text'] = data['full_text'].str.strip()
    data["full_text"] = data["full_text"].apply(remove_likely_table_blocks)

    data['concepts'] = data['concepts'].apply(extract_inner_args, args=('display_name',))
    data['primary_location'] = data['primary_location'].apply(extract_landing_page)
    data['keywords'] = data['keywords'].apply(extract_inner_args, args=('display_name',))

    data['authorships'] = data['authorships'].apply(extract_inner_args, args=('author',))
    data['authorships_names'] = data['authorships'].apply(extract_inner_args, args=('display_name',))
    data['authorships_orcid'] = data['authorships'].apply(extract_inner_args, args=('orcid',))
    data = data.drop(columns=['authorships'])

    data = expand_dict_columns(data, 'biblio')

    data.to_json(file_path, orient='records', force_ascii=False)