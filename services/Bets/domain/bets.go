package domain

import "context"

type Bet struct {
	Login   string `bson:"login"`
	MatchID string `bson:"matchid"`
	TeamPos int32  `bson:"teampos"`
	Amount  int32  `bson:"amount"`
}

type Debit struct {
	Login  string
	Amount int32
}

type UserClient interface {
	Withdraw(ctx context.Context, d Debit) error
}

type BetRepository interface {
	Place(ctx context.Context, b Bet) error
	AllBetsOnMatch(ctx context.Context, matchID string) ([]Bet, error)
}
