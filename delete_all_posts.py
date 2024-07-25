import requests, time
from requests.auth import HTTPBasicAuth

# Your WordPress site URL
wp_site_url = '{Your website url}'
# Your REST API endpoint for posts
wp_api_endpoint = f'{wp_site_url}/wp-json/wp/v2/posts'
# Your WordPress username and application password
wp_username = '{Your username}'
wp_app_password = '{Your password}'
wp_bearer_token = "{Your token}"  # Your Bearer token

def get_all_posts(status='any'):
    """Get all posts from the WordPress site with the specified status."""
    posts = []
    page = 1

    while True:
        response = requests.get(
            wp_api_endpoint, 
            headers={'Authorization': f'Bearer {wp_bearer_token}'}, 
            params={'per_page': 100, 'page': page, 'status': status}
        )

        if response.status_code == 400:
            error_data = response.json()
            if error_data.get('code') == 'rest_post_invalid_page_number':
                print(f"No more posts found. Total pages fetched: {page-1}")
                break
            else:
                raise Exception(f'Error fetching posts: {response.status_code} - {response.text}')
        
        if response.status_code != 200:
            raise Exception(f'Error fetching posts: {response.status_code} - {response.text}')
        
        current_posts = response.json()
        if not current_posts:
            print(f"No posts found on page {page}. Stopping pagination.")
            break

        print(f"Fetched {len(current_posts)} posts from page {page}.")
        posts.extend(current_posts)
        page += 1

    return posts

def delete_post(post_id):
    """Delete a single post by ID."""
    delete_endpoint = f'{wp_api_endpoint}/{post_id}?force=true'
    response = requests.delete(
        delete_endpoint, 
        headers={'Authorization': f'Bearer {wp_bearer_token}'}
    )

    if response.status_code == 200:
        print(f'Successfully deleted post with ID {post_id}')
    else:
        print(f'Failed to delete post with ID {post_id}: {response.status_code} - {response.text}')
        time.sleep(1)  # Wait for a second before retrying to avoid rate limits

def delete_all_posts():
    """Delete all posts from the WordPress site."""
    # Change the status as needed ('publish', 'draft', 'pending', 'private', etc.)
    posts = get_all_posts(status='any')

    if not posts:
        print('No posts found to delete.')
        return

    print(f"Total posts to delete: {len(posts)}")

    for post in posts:
        delete_post(post['id'])
        time.sleep(0.5)  # Add a small delay to avoid hitting the rate limit

if __name__ == '__main__':
    delete_all_posts()
