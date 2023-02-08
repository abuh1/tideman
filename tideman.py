import sys
from itertools import combinations

if len(sys.argv) < 2:
    print("Usage: python tideman.py candidates")
    sys.exit()
elif len(sys.argv) > 10:
    print("Maximum number of candidates allowed is 9")
    sys.exit()
else:
    candidates = [names.capitalize() for names in sys.argv[1:]]

# Class for each pair of candidates
class Pair:
    def __init__(self, pair, ballots):
        self.ballots = ballots
        self.pair = pair
        self.cand_a = pair[0]
        self.cand_b = pair[1]
        self.winner, self.loser = None, None
        self.win_margin = 0
    
    # Returns winner, loser, and win margin of pair  
    def calculate_results(self):
        a_wins, b_wins = 0, 0
        a_index, b_index = None, None
        for votes in self.ballots:
            # Key values for both candidates in ballots dictionaries
            a_key = next(k for k,v in votes.items() if v == self.cand_a)
            b_key = next(k for k,v in votes.items() if v == self.cand_b)
            # Index of both candidates in ballot
            a_index = list(votes.keys()).index(a_key)
            b_index = list(votes.keys()).index(b_key)
            # Checking if candidate a is ranked higher than b or vice versa
            if a_index < b_index:
                a_wins += 1
            else:
                b_wins += 1
        # Calculate the win margin of the winner candidate
        self.win_margin = abs(a_wins - b_wins)
        # Choose winner, loser and win margin
        if a_wins > b_wins:
            self.winner = self.cand_a
            self.loser = self.cand_b
        elif b_wins > a_wins:
            self.winner = self.cand_b
            self.loser = self.cand_a
        else:
            self.winner = self.cand_a
            self.loser = self.cand_b
            self.win_margin = 0
    
    def get_winner(self):
        return self.winner
    
    def get_loser(self):
        return self.loser
    
    def get_win_margin(self):
        return self.win_margin
                

# Main function
def main():
    # List of dictionaries for each ballot (rank : name)
    ballots = []
    # Get number of voters, and user ranks each candidate for each voter
    while True:
        try:
            num_voters = int(input('Number of voters: '))
        except ValueError:
            print("Please enter a number.")
            continue
        else:
            break
        
    # Creates list of pair objects of type Pair
    pairs = []
    for comb in combinations(candidates, 2):
        new_pair = Pair(comb, ballots)
        pairs.append(new_pair)
    
    for i in range(num_voters):
        print("-" * 60)
        print(f"Ballot Number {i + 1}")
        
        ranks = {}
        vote_candidate(ranks)
                
        ballots.append(ranks)
    
    # Append winner and loser in order of margin win. At the end, deletes last pair if it is a stalemate situation.
    final_results = sort_victories(pairs)
    pair_winners = []
    pair_losers = []
    for r in final_results:
        pair_winners.append(r[0].get_winner())
        pair_losers.append(r[0].get_loser())
    if set(candidates).issubset(pair_winners) and set(candidates).issubset(pair_losers):
        del pair_winners[-1]
        del pair_losers[-1]
    
    # Returns the winner (the candidate that is not in pair_losers list)
    for c in candidates:
        if c not in pair_losers:
            final_winner = c
    print("WINNER: ", final_winner)
    

# Function to vote ranks for each candidate in each ballot
def vote_candidate(ranks):
    for cand in range(len(candidates)):
        # Keep asking for same rank if input is invalid
        while True:
            vote = input(f"Rank {cand + 1}: ")
            vote = vote.capitalize()
            if vote not in candidates or vote in ranks.values():
                print("Candidate does not exist or has already been voted")
            elif vote in candidates:
                ranks[f"Rank {cand + 1}"] = vote
                break

# Sort each pair of candidates in decreasing strength of victory. Sorted using quick_sort function
def sort_victories(pairs):
    sorted_pairs = {}
    for p in pairs:
        p.calculate_results()
        if p.get_winner() != None:
            sorted_pairs[p] = p.get_win_margin()
            
    sorted_pairs = sorted(sorted_pairs.items(), reverse=True, key=lambda item: item[1])
    return sorted_pairs
    


if __name__ == '__main__':
    main()