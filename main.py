import dotenv
import argparse
import twitter
import os


class HashableUser(object):
    def __init__(self, user: twitter.User):
        self.user = user

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.user.id == other.user.id

    def __hash__(self):
        return self.user.id

    def __str__(self):
        return f"{self.user.name}, https://twitter.com/{self.user.screen_name}"


def main(dry_run: bool = True):
    api = twitter.Api(
        consumer_key=os.environ['CONSUMER_KEY'],
        consumer_secret=os.environ['CONSUMER_SECRET'],
        access_token_key=os.environ['ACCESS_TOKEN'],
        access_token_secret=os.environ['ACCESS_TOKEN_SECRET'],
    )

    followings = set(map(lambda u: HashableUser(u), api.GetFriends()))
    list_members = []
    lists = []
    for l in api.GetLists():
        l_members = list(map(lambda u: HashableUser(u), api.GetListMembers(l.id)))
        list_members += l_members
        lists.append((l.name, set(l_members)))
    list_members = set(list_members)

    print(f"You are following {len(followings)} users")
    print(f"You have {len(list_members)} list members")

    # followings who are not a list member
    unsanctioned_followings = followings - list_members
    print(f"You are about to un-follow {len(unsanctioned_followings)} because they do not belong to any list")
    for f in unsanctioned_followings:
        print(f"Unfollowing {str(f)}")
        if not dry_run:
            api.DestroyFriendship(user_id=f.user.id)

    # list member who I am not following
    unfollowed_list_members = list_members - followings
    print(f"You are about to follow {len(unfollowed_list_members)} because they belong to a list but not followed")
    for f in list_members - followings:
        print(f"Following {str(f)}")
        if not dry_run:
            api.CreateFriendship(user_id=f.user.id, follow=False, retweets=False)

    # lists are mutually exclusive
    for i in range(len(lists)):
        for j in range(i + 1, len(lists)):
            (l1_name, l1), (l2_name, l2) = lists[i], lists[j]
            print(f"Checking mutual exclusivity between {l1_name} and {l2_name}")
            for dup_user in l1.intersection(l2):
                print(f"Lists {l1_name} and {l2_name} share user {str(dup_user)}")


if __name__ == '__main__':
    dotenv.load_dotenv()

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--dry-run', choices=['true', 'false'], default='true')
    args = arg_parser.parse_args()

    main(args.dry_run != 'false')
