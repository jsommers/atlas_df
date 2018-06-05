def transform_df(df, transformations):
    for t in transformations.get('apply', []):
        if len(t) == 2:
            df[t[0]] = df[t[0]].apply(t[1])
        elif len(t) == 3:
            df[t[1]] = df[t[0]].apply(t[2])

    for t in transformations.get('astype', []):
        df[t[0]] = df[t[0]].astype(t[1])

    for t in transformations.get('replace', []):
        df[t[0]].replace(t[1], t[2], inplace=True)

    if 'geometry' in transformations:
        df.set_geometry(transformations['geometry'], inplace=True)

    if 'index' in transformations:
        df.set_index(transformations['index'], inplace=True)
