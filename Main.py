# https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28#event-object-common-properties

import requests
import json

def get_events(username):
    try:
        # get events for specified user
        url = f"https://api.github.com/users/{username}/events"
        response = requests.get(url)
        
        # check status code
        status_code = response.status_code
        match status_code:
            case 200:
                events = response.json()
                for e in events:
                    # gather common properties for events
                    event_type = e['type']
                    user = e['actor']['login']
                    repo = e['repo']['name']
                    date = e['created_at']

                    # Check event type and return a message for each situation:
                    # A commit comment is created
                    if event_type == "CommitCommentEvent":
                        comment = e['payload']['comment']['body']
                        print(f"[{date}] > @{user} commented on a commit in {repo}: '{comment}'")
                    # A Git branch or tag is created
                    elif event_type == "CreateEvent": 
                        ref_type = e['payload']['ref_type']
                        ref = e['payload']['ref']
                        if ref_type == "branch":
                            print(f"[{date}] > @{user} created a new branch in {repo} called {ref}")
                        elif ref_type == "repository":
                            print(f"[{date}] > @{user} created a new repository called {repo}")
                        else:
                            print(f"[{date}] > @{user} created a new {ref_type}")
                    # A Git branch or tag is deleted
                    elif event_type == "DeleteEvent": 
                        ref_type = e['payload']['ref_type']
                        ref = e['payload']['ref']
                        print(f"[{date}] > @{user} deleted {ref_type} '{ref}' from {repo}")
                    # A user forks a repository
                    elif event_type == "ForkEvent": 
                        forkee = e['payload']['forkee']
                        print(f"[{date}] > @{user} forked {repo} --> {forkee}")
                    # A wiki page is created or updated
                    elif event_type == "GollumEvent":
                        print(f"[{date}] > @{user} modified the wiki page(s) in {repo}")
                    # Activity related to an issue or pull request comment
                    elif event_type == "IssueCommentEvent":
                        comment = e['payload']['comment']['body']
                        print(f"[{date}] > @{user} posted a comment in {repo}: '{comment}'")
                    # Activity related to an issue
                    elif event_type == "IssuesEvent":
                        action = e['payload']['action']
                        print(f"[{date}] > @{user} {action} an issue in {repo}")
                    # Activity related to repository collaborators
                    elif event_type == "MemberEvent":
                        user_added = e['payload']['member']
                        print(f"[{date}] > @{user} added {user_added} as a member to {repo}")
                    # When a private repository is made public
                    elif event_type == "PublicEvent":
                        print(f"[{date}] > @{user} changed {repo} from private to public")
                    # Activity related to pull requests
                    elif event_type == "PullRequestEvent":
                        pr_num = e['payload']['number']
                        action = e['payload']['action']
                        print(f"[{date}] > @{user} performed the following action on {repo} pull request {pr_num}: {action}")
                    # Activity related to pull request reviews
                    elif event_type == "PullRequestReviewEvent":
                        action = e['payload']['action']
                        print(f"[{date}] > @{user} reviewed a pull request in {repo}")
                    # Activity related to pull request review comments in the pull request's unified diff
                    elif event_type == "PullRequestReviewCommentEvent":
                        print(f"[{date}] > @{user} left a comment on a pull request in {repo}")
                    # Activity related to a comment thread on a pull request being marked as resolved or unresolved
                    elif event_type == "PullRequestReviewThreadEvent":
                        action = e['payload']['action']
                        print(f"[{date}] > @{user} marked a pull request as {action} in {repo}")
                    # One or more commits are pushed to a repository branch or tag
                    elif event_type == "PushEvent":
                        push_id = e['payload']['push_id']
                        num_of_commits = e['payload']['size']
                        print(f"[{date}] > @{user} pushed {num_of_commits} commit(s) to {repo} (Push ID {push_id})")
                    # Activity related to a release
                    elif event_type == "ReleaseEvent":
                        action = e['payload']['action']
                        print(f"[{date}] > @{user} {action} a release in {repo}")
                    # Activity related to a sponsorship listing
                    elif event_type == "SponsorshipEvent":
                        action = e['payload']['action']
                        effective_date = e['payload']['effective_date']
                        print(f"[{date}] > @{user} {action} a sponsorship listing in {repo}, effective {effective_date}")
                    # When someone stars a repository
                    elif event_type == "WatchEvent":
                        print(f"[{date}] > @{user} starred the repository {repo}")
                    else:
                        print(f"[{date}] > ***unhandled event for event type {event_type}***")
            case 304:
                print(f"{status_code} - Not modified")
            case 403:
                print(f"{status_code} - Forbidden")
            case 503:
                print(f"{status_code} - Service Unavailable")
            case _:
                print(f"Error: {status_code} - Unable to fetch events for user {username}")
    except Exception as e:
        print(f"An unexpected error has occured: {e}")
if __name__ == "__main__":
    user = input("Enter GitHub username: ")
    get_events(user) 