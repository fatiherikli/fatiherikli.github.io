import os
import yaml

def get_album_paths(path='photos'):
  yield from (
    os.path.join(path, name)
    for name in os.listdir(path)
    if name.endswith('yaml')
  )

def load_meta(path):
  return yaml.load(open(path))

def parse(content, context):
  return content.format(**context)

def build_template(name, **context):
  path = 'templates/%s' % name
  return parse(open(path).read(), context)

def render_photo(photo):
  return build_template('photo-item.html', **photo)

def render_photos(photos):
  return '\n'.join(map(render_photo, photos))

def render_album(album):
  return build_template(
    'album-template.html',
    rendered_photos=render_photos(album['photos']),
    **album
  )

def get_album_metas():
  return map(load_meta, get_album_paths())

def generate_albums():
  posts = get_album_metas()

  for post in posts:
    open(
      post['file'],
      'w'
    ).write(
      render_album(post)
    )

if __name__ == "__main__":
  generate_albums()
