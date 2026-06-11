import sys, time, random
from collections import deque, defaultdict

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    def shortest_path_ans(self, path, goal_id):
        ans = []
        ans_id = [goal_id]
        i = goal_id
        while True:
            if path[i] == -1:
                break
            ans_id.append(path[i])
            i = path[i]
        for id in ans_id:
            ans.append(self.titles[id])
        return ans

    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        start_id = len(self.titles) + 1
        goal_id = len(self.titles) + 1

        for id in self.titles.keys():
            if self.titles[id] == start:
                start_id = id
            if self.titles[id] == goal:
                goal_id = id

        if start_id == len(self.titles) + 1 or goal_id == len(self.titles) + 1:
            print("スタートまたはゴールが存在しません。")
            exit(1)

        deq = deque()
        deq.append(start_id)
        path = {start_id: -1}
        seen = defaultdict(bool)
        seen = set([start_id])
        while len(deq) != 0:
            index = deq.popleft()
            for i in self.links[index]:
                if i not in seen:
                    path[i] = index
                    if i == goal_id:
                        print(self.shortest_path_ans(path, goal_id))
                        print()
                        return True
                    deq.append(i)
                    seen.add(i)
        pass


    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        pre_ans_page_rank = defaultdict(lambda: 1)
        while True:
            ans_page_rank = defaultdict(lambda: 0)
            sum_page_rank = len(self.titles.keys()) * 0.15 # 最後に分配する用
            for id in self.titles.keys():
                for i in self.links[id]:
                    ans_page_rank[i] += pre_ans_page_rank[id] * 0.85 / len(self.links[id])
                if len(self.links[id]) == 0:
                    sum_page_rank += pre_ans_page_rank[id] * 0.85
            for id in self.titles.keys():
                ans_page_rank[id] += sum_page_rank / len(self.titles.keys())

            cnt = 0
            for id in self.titles.keys():
                cnt += (ans_page_rank[id] - pre_ans_page_rank[id]) * (ans_page_rank[id] - pre_ans_page_rank[id])
            if cnt < 0.01:
                break
            pre_ans_page_rank = ans_page_rank


        sorted_ans_page_rank = sorted(ans_page_rank.items(), key=lambda x:x[1], reverse=True)
        for i in range(10):
            x, y = sorted_ans_page_rank[i]
            print(str(i+1) + ": " + self.titles[x])
        pass


    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        random.seed(1)

        # スタートとゴールのidを探す
        start_id = len(self.titles) + 1
        goal_id = len(self.titles) + 1
        for id in self.titles.keys():
            if self.titles[id] == start:
                start_id = id
            if self.titles[id] == goal:
                goal_id = id
        if start_id == len(self.titles) + 1 or goal_id == len(self.titles) + 1:
            print("スタートまたはゴールが存在しません。")
            exit(1)

        # 出次数の昇順でソート
        sorted_links_list = defaultdict()
        for id in self.titles.keys():
            sorted_links_list[id] = sorted(self.links[id], key=lambda x: len(self.links[x]), reverse=True)

        seen = set([start_id])
        stack = [[start_id, list(sorted_links_list[start_id])]]
        best_path_ids = []
        max_len = 0

        start_time = time.time()
        time_limit = 60.0 # 探索を続ける時間

        while len(stack) != 0:
            current_time = time.time()
            if time_limit < current_time - start_time:
                break

            current_id, neighbors = stack[-1]

            # ゴールに辿り着いたかどうか
            if current_id == goal_id:
                path_ids = [item[0] for item in stack]
                if len(path_ids) > max_len:
                    max_len = len(path_ids)
                    best_path_ids = list(path_ids)

                # 少し前から探索し直す
                max_backtrack = min(100, len(stack) - 1)
                backtrack_steps = random.randint(1, max_backtrack)
                for _ in range(backtrack_steps):
                    pre_id = stack.pop()[0]
                    seen.remove(pre_id)
                continue

            # 未訪問の隣接頂点を探す
            found_next = False
            while len(neighbors) > 0:
                next_id = neighbors.pop()
                if next_id not in seen:
                    seen.add(next_id)
                    stack.append([next_id, list(sorted_links_list[next_id])])
                    found_next = True
                    break

            # 探索できる隣接ノードがなければ一つ前の頂点に戻る
            if not found_next:
                popped_node, _ = stack.pop()
                seen.remove(popped_node)

        if max_len > 0:
            self.assert_path(best_path_ids, start, goal)
            ans = [self.titles[id] for id in best_path_ids]
            print("最長経路の長さは" + str(len(ans)))
            print("パスの先頭から最大で10個まで出力")
            for i in range(min(10, len(ans))):
                print(str(i+1) + ans[i])
        else:
            print("パスが見つかりませんでした。")
        pass


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])
        visited = {}
        for node in path:
            assert(node not in visited)
            visited[node] = True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    wikipedia.find_longest_titles()
    # Example
    wikipedia.find_most_linked_pages()
    # Homework #1
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")