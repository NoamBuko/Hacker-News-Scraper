import requests
import csv
import pandas as pd
import matplotlib.pyplot as plt

def hacker_news_scraper(story_output_path, comment_outputh_path, stat_output_path, num_of_stories):
    '''
    Scrapes data from the top stories if the hacker news site, and saves all the data in csv files.
    Arguments: output paths for each of the csv files, and the sum of top dtories to scrape.
    '''
    # Save the IDs of the top stories in a list
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    response = requests.get(url)
    top_stories = response.json()

    scrape_stories(top_stories, num_of_stories, story_output_path)
    scrape_comments(top_stories, num_of_stories, comment_outputh_path)
    analyze_and_plot_data(story_output_path, stat_output_path)



def scrape_stories(top_stories, num_of_stories, output_path):
    # Create csv file and save the info
    with open(output_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Title', 'URL', 'Author', 'Score', 'Num_Comments', 'Time'])

        for story_id in top_stories[:num_of_stories]:
            # Get story info
            story_url = 'https://hacker-news.firebaseio.com/v0/item/' + str(story_id) + '.json'
            response = requests.get(story_url)
            dict = response.json()

            # Check if the story has all the feilds, and if so write relevant info to the csv file
            if all(key in dict for key in ('id', 'title', 'url', 'by', 'score', 'descendants', 'time')):
                writer.writerow([dict['id'], dict['title'], dict['url'], dict['by'], dict['score'], dict['descendants'], dict['time']])
            
        print(f'Finished to scrape stories, saved to {output_path}')
    return


def scrape_comments(top_stories, num_of_stories, output_path):
    # Create csv file and save the info
    with open(output_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Author', 'Text', 'Time', 'Parent Story ID'])

        for story_id in top_stories[:num_of_stories]:
            # Get comment info for each comment on every story
            story_url = 'https://hacker-news.firebaseio.com/v0/item/' + str(story_id) + '.json'
            response = requests.get(story_url)
            dict = response.json()
            if 'kids' in dict:
                comments = dict['kids']
                for comment in comments:
                    comment_url = 'https://hacker-news.firebaseio.com/v0/item/' + str(comment) + '.json'
                    comment_response = requests.get(comment_url)
                    comment_dict = comment_response.json()
                    if all(key in comment_dict for key in ('by', 'text', 'time', 'parent')):
                        writer.writerow([comment_dict['by'], comment_dict['text'], comment_dict['time'], comment_dict['parent']])
        print(f'Finished to scrape comments, saved to {output_path}')
    return


def analyze_and_plot_data(stories_csv_file, output_path):
    # We will analyze the score and num_of_comments columns of the stories.csv file
    data_frame = pd.read_csv(stories_csv_file)
    scores_list = data_frame['Score'].to_list()
    num_comments_list = data_frame['Num_Comments'].tolist()

    # Calculate the statistics 
    min_score = min(scores_list)
    max_score = max(scores_list)
    average_score = sum(scores_list) / len(scores_list)

    min_num_comments = min(num_comments_list)
    max_num_comments = max(num_comments_list)
    average_num_comments = sum(num_comments_list) / len(num_comments_list)

    # Write stats to output csv file 
    with open(output_path, 'w') as file:
        writer = csv.writer(file)
        stats = ['Min Score', 'Max Score', 'Average_Score', 'Min_Comments', 'Max Comments', 'Average_comments']
        values = [min_score, max_score, average_score, min_num_comments, max_num_comments, average_num_comments]
        writer.writerows([stats, values])
        
    plot_stats(stats, values)


def plot_stats(x_list, y_list):
    plt.figure(figsize=(12, 7))
    plt.bar(x_list, y_list, color='skyblue')
    plt.xlabel('Stats')
    plt.ylabel('Values')
    plt.title('Stats from scraper')
    plt.show()


hacker_news_scraper('story.csv', 'comment.csv', 'stat.csv', 3)
