import random

# define a table for face cards
card_name = {
	1 : "ACE",
	2 : "2",
	3 : "3",
	4 : "4",
	5 : "5",
	6 : "6",
	7 : "7",
	8 : "8",
	9 : "9",
	10 : "10",
	11 : "JACK",
	12 : "QUEEN",
	13 : "KING"
}

# define a object consists of suit and number
class Poker:
	def __init__(self, suit, num):
		self._suit = suit
		self._num = num

# to compute the value of hand
def value_compute(hand):
	hand_num = list()
	for card in hand:
		hand_num.append(card._num)

	value = 0
	ace_num = 0
	for num in hand_num:
		if num == 1:
			ace_num+=1
			value+=11
		elif num > 10:
			value+=10
		else:
			value+=num

	# consider the ACE as 1 if the total value > 21
	for i in range(ace_num):
		if value>21:
			value-=10

	if value > 21:
		return "Busts! (>21)"
	elif value == 21:
		return "Blackjack! (21)"
	else:
		return value

# player's move
def Player_turn(deck):
	player_hand = []
	player_hand.append(deck.pop())
	player_hand.append(deck.pop())

	while(True):
		player_val = value_compute(player_hand)
		print("Your current value is " + str(player_val))
		print("with the hand: ")
		for card in player_hand:
			suit = card._suit
			num = card._num
			print(card_name.get(num, None)+"-"+suit+" ", end="")
		print(" ")

		if player_val ==  "Busts! (>21)":
			return player_val, deck

		hit_or_stay = input("Hit or stay? (Hit = 1, Stay = 0): ")

		if hit_or_stay == "0":
			print(" ")
			return player_val, deck
		else:
			card_draw = deck.pop()
			player_hand.append(card_draw)
			print("You draw "+card_name.get(card_draw._num, None)+"-"+card_draw._suit+"\n")

# dealer's move
def Dealer_turn(deck):
	dealer_hand = []
	dealer_hand.append(deck.pop())
	dealer_hand.append(deck.pop())

	while(True):
		dealer_val = value_compute(dealer_hand)
		print("Dealer's current value is " + str(dealer_val))
		print("with the hand: ")
		for card in dealer_hand:
			suit = card._suit
			num = card._num
			print(card_name.get(num, None)+"-"+suit+" ", end="")
		print(" ")

		if dealer_val=="Busts! (>21)" or dealer_val=="Blackjack! (21)":
			return dealer_val

		if dealer_val >= 17:
			return dealer_val
		else:
			card_draw = deck.pop()
			dealer_hand.append(card_draw)
			print("\nDealer draws "+card_name.get(card_draw._num, None)+"-"+card_draw._suit+"\n")
			continue



# create a new game
def Game(deck):
	random.shuffle(deck)

	player_val, deck_remain = Player_turn(deck)

	if player_val == "Busts! (>21)":
		print("\n*** Dealer wins! ***")
	else:
		# if player's value isn't busts
		dealer_val = Dealer_turn(deck)

		if dealer_val == "Busts! (>21)":
			print("\n*** You beat the Dealer! ***")

		elif dealer_val == "Blackjack! (21)":
			if player_val == "Blackjack! (21)":
				print("\n*** You tied the dealer, nobody wins. ***")
			else:
				print("\n*** Dealer wins! ***")
		# when dealer's value < 21
		else:
			if player_val == "Blackjack! (21)":
				print("\n*** You beat the Dealer! ***")
			elif dealer_val > player_val:
				print("\n*** Dealer wins! ***")
			elif dealer_val == player_val:
				print("\n*** You tied the dealer, nobody wins. ***")
			else:
				print("\n*** You beat the Dealer! ***")



		

# create a complete poker deck
deck = list()
for i in range(13):
	deck.append(Poker('SPADE', i+1))
	deck.append(Poker('HEART', i+1))
	deck.append(Poker('DIAMOND', i+1))
	deck.append(Poker('CLUB', i+1))

while(True):
	Game(deck.copy())

	again_or_not = input("Want to play again? (y/n): ")
	print(" ")
	if again_or_not == "y":
		continue
	else:
		break










