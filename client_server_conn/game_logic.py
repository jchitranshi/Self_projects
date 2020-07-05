def game_logic(you,opponent):
	winner=""
	rock="rock"
	paper="paper"
	scissors="scissors"
	player0=you
	player1=opponent

	if you==opponent:
		winner=='draw'
	elif you==rock:
		if opponent==paper:
			winner=player1
		else:
			winner=player0
	elif you==paper:
		if opponent==rock:
			winner=player0
		else:
			winner=player1
	else:
		if opponent==paper:
			winner=player0
		else:
			winner=player1
	return winner
		