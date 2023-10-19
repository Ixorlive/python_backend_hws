package domain

import (
	"context"
	"errors"
)

type Match struct {
	ID        string
	Team1     string
	Team2     string
	MatchTime string
	Status    MatchStatus
}

type MatchStatus int32

const (
	Upcoming MatchStatus = iota
	Ongoing
	Completed
)

type MatchRepository interface {
	AddMatch(ctx context.Context, m Match) (Match, error)
	UpdateMatchTime(ctx context.Context, id string, newTime string) (Match, error)
	MarkMatchAsCompleted(ctx context.Context, id string) (Match, error)
	ListMatches(ctx context.Context, status MatchStatus) ([]Match, error)
}

var ErrMatchNotFound = errors.New("match not found")
