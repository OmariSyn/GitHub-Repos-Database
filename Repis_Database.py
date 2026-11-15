import json
import redis

# Connect to local Redis instance
client = redis.Redis(host='localhost', port=6379, decode_responses=True)


def feature_load_and_list():
  """Feature 1: Load sample JSON into Redis and list top repositories."""
  print('\n--- [Feature 1] Load & List Repositories ---')
  try:
    with open('Sample_Repos.json', 'r', encoding='utf-8') as f:
      count = 0
      for line in f:
        if line.strip():
          data = json.loads(line)
          name, watches = data['repo_name'], int(data['watch_count'])
          client.hset(f'repo:{name}', mapping={'watch_count': watches})
          client.zadd('github:repos', {name: watches})
          count += 1
    print(f'Successfully loaded {count} repositories from file.')
  except FileNotFoundError:
    print("Notice: 'Sample_Repos.json' not found. Skipping auto-load.")

  # Display top 5
  print('\nTop Repositories in Database:')
  top = client.zrevrange('github:repos', 0, 4, withscores=True)
  if not top:
    print('  (Database is currently empty)')
  for i, (name, watches) in enumerate(top, 1):
    print(f'  {i}. {name} — {int(watches)} watches')


def feature_add_or_update():
  """Feature 2: Add a new repo or update an existing one."""
  print('\n--- [Feature 2] Add / Update Repository ---')
  name = input('Enter repository name (owner/repo): ').strip()
  try:
    watches = int(input('Enter watch count: ').strip())
  except ValueError:
    print('Error: Watch count must be a valid integer.')
    return

  client.hset(f'repo:{name}', mapping={'watch_count': watches})
  client.zadd('github:repos', {name: watches})
  print(f"Success: '{name}' updated with {watches} watches.")


def feature_delete():
  """Feature 3: Delete a repository from the database."""
  print('\n--- [Feature 3] Delete Repository ---')
  name = input('Enter repository name to delete: ').strip()

  deleted_hash = client.delete(f'repo:{name}')
  deleted_zset = client.zrem('github:repos', name)

  if deleted_hash or deleted_zset:
    print(f"Success: '{name}' has been deleted.")
  else:
    print(f"Notice: Repository '{name}' was not found.")


# --- Main Menu Loop ---
if __name__ == '__main__':
  while True:
    print('\n============================')
    print('   REDIS REPO MANAGER (3-in-1)')
    print('============================')
    print('1. Load JSON & List Top Repos')
    print('2. Add or Update a Repo')
    print('3. Delete a Repo')
    print('4. Exit')

    choice = input('Choose an option (1-4): ').strip()

    if choice == '1':
      feature_load_and_list()
    elif choice == '2':
      feature_add_or_update()
    elif choice == '3':
      feature_delete()
    elif choice == '4':
      print('Exiting. Goodbye!')
      break
    else:
      print('Invalid choice. Please pick 1, 2, 3, or 4.')