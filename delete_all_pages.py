import requests
import time

# Your WordPress site URL
wp_site_url = '{Your website url}'
# Your REST API endpoint for pages
wp_api_endpoint = f'{wp_site_url}/wp-json/wp/v2/pages'
# Your WordPress username and application password
wp_username = '{Your username}'
wp_app_password = '{Your password}'
wp_bearer_token = "{Your bearer token}"  # Your Bearer token

def get_all_pages(status='any'):
    """Get all pages from the WordPress site with the specified status."""
    pages = []
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
                print(f"No more pages found. Total pages fetched: {page-1}")
                break
            else:
                raise Exception(f'Error fetching pages: {response.status_code} - {response.text}')
        
        if response.status_code != 200:
            raise Exception(f'Error fetching pages: {response.status_code} - {response.text}')
        
        current_pages = response.json()
        if not current_pages:
            print(f"No pages found on page {page}. Stopping pagination.")
            break

        print(f"Fetched {len(current_pages)} pages from page {page}.")
        pages.extend(current_pages)
        page += 1

    return pages

def delete_page(page_id):
    """Delete a single page by ID."""
    delete_endpoint = f'{wp_api_endpoint}/{page_id}?force=true'
    response = requests.delete(
        delete_endpoint, 
        headers={'Authorization': f'Bearer {wp_bearer_token}'}
    )

    if response.status_code == 200:
        print(f'Successfully deleted page with ID {page_id}')
    else:
        print(f'Failed to delete page with ID {page_id}: {response.status_code} - {response.text}')
        time.sleep(1)  # Wait for a second before retrying to avoid rate limits

def delete_all_pages():
    """Delete all pages from the WordPress site."""
    # Change the status as needed ('publish', 'draft', 'pending', 'private', etc.)
    pages = get_all_pages(status='any')

    if not pages:
        print('No pages found to delete.')
        return

    print(f"Total pages to delete: {len(pages)}")

    for page in pages:
        delete_page(page['id'])
        time.sleep(0.5)  # Add a small delay to avoid hitting the rate limit

if __name__ == '__main__':
    delete_all_pages()
