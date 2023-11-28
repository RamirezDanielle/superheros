from flask import Flask, request, render_template, redirect, session
import os 
import requests


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    superhero_name = None
    if request.method == 'POST':
        search = request.form['search']
        headers = os.environ.get("KEY")
        search_url = f"https://superheroapi.com/api/{headers}/search/{search}"
        response = requests.get(search_url)
        if response.status_code == 200:
            data = response.json()
            # Check if the 'results' key is present in the response
            if 'results' in data:
                # Get the first superhero in the results 
                superhero = data['results'][0]
                # Extract the superhero ID
                superhero_id = superhero['id']
                #the URL for getting the superhero image
                superhero_name = superhero.get('name', 'Unknown Superhero')
                image_url = f"https://superheroapi.com/api/{headers}/{superhero_id}/image"
                # Make the request to get the superhero image
                image_response = requests.get(image_url)
                # Check if the image request was successful
                if image_response.status_code == 200:
                    # Get the image URL from the response
                    image_data = image_response.json()
                    image_url = image_data.get('url', 'Image URL not available')
                    # Render the template with the image URL
                    return render_template('index.html', image_url=image_url, superhero_name=superhero_name, error_message=None)
                else:
                    return render_template('index.html', image_url=None, superhero_name=superhero_name, error_message=f"Error getting superhero image: {image_response.status_code}")
            else:
                return render_template('index.html', image_url=None, superhero_name=superhero_name, error_message=f"Nice try Nerd..No results found for superhero: {search}")
        else:
            return render_template('index.html', image_url=None, superhero_name=superhero_name, error_message=f"Error searching for superhero: {response.status_code}")

    # For GET requests, render the index template
    return render_template('index.html', image_url=None, superhero_name=None, error_message=None)


# @app.route('/get_superhero', methods=['POST'])
# def get_superhero():
#     search = request.form['search']
#     print(search)
#     headers = os.environ.get("KEY")
#     search_url = f"https://superheroapi.com/api/{headers}/search/{search}"
#     print(search_url)
#     response = requests.get(search_url)
#     print(response.json())
#     if response.status_code == 200:
#         # Parse the response JSON
#         data = response.json()
#         # Check if the 'results' key is present in the response
#         if 'results' in data:
#             # Get the first superhero in the results
#             superhero = data['results'][0]
#             # Extract the superhero ID
#             superhero_id = superhero['id']
#             # Construct the URL for getting the superhero image
#             image_url = f"https://superheroapi.com/api/{headers}/{superhero_id}/image"
#             # Make the request to get the superhero image
#             image_response = requests.get(image_url)
#             # Check if the image request was successful
#             if image_response.status_code == 200:
#                 # Get the image URL from the response
#                 image_data = image_response.json()
#                 image_url = image_data.get('url', 'Image URL not available')
#                 # Render a template or return the image URL as needed
#                 return render_template('index.html', image_url=image_url, error_message=None)
#             else:
#                 return render_template('index.html', image_url=None, error_message=f"Error getting superhero image: {image_response.status_code}")
#         else:
#             return render_template('index.html' , image_url=None, error_message =f"Nice try nerd.. no results found for superhero: {search}")
#     else:
#         return render_template('index.html', image_url=None, error_message =f"Error searching for superhero: {response.status_code}")
    # return 


if __name__=='__main__':
    app.run(debug=True)