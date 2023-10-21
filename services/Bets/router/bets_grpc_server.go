package router

import (
	"Bets/domain"
	pb "Bets/proto_gen/betservicepb"
	"context"
)

// BetGRPCServer represents the gRPC server for managing bets.
type BetGRPCServer struct {
	pb.UnimplementedBetsServer

	repo       domain.BetRepository
	userClient domain.UserClient
}

// NewBetGRPCServer creates a new instance of BetGRPCServer.
func NewBetGRPCServer(r domain.BetRepository, userClient domain.UserClient) *BetGRPCServer {
	return &BetGRPCServer{repo: r, userClient: userClient}
}

const successPlaceBetMessage = "The bet was placed successfully"

// Place processes the placing of a bet.
func (s *BetGRPCServer) PlaceBet(ctx context.Context, req *pb.PlaceBetRequest) (*pb.Confirmation, error) {
	err := s.userClient.Withdraw(ctx, domain.Debit{
		Login:  req.GetLogin(),
		Amount: req.GetAmount(),
	})

	if err != nil {
		return confirmError(err)
	}

	bet := domain.Bet{
		Login:   req.GetLogin(),
		MatchID: req.GetMatchID(),
		TeamPos: req.GetTeamPos(),
		Amount:  req.GetAmount(),
	}

	err = s.repo.Place(ctx, bet)
	if err != nil {
		return confirmError(err)
	}

	return &pb.Confirmation{
		Success: true,
		Message: successPlaceBetMessage,
	}, nil
}

// CalculateOddsRequest calculates the odds for a given match.
func (s *BetGRPCServer) CalculateOdds(ctx context.Context, req *pb.CalculateOddsRequest) (*pb.CalculateOddsResponse, error) {
	bets, err := s.repo.AllBetsOnMatch(ctx, req.GetMatchID())
	if err != nil {
		return nil, err
	}

	var totalBetOnTeam1 int32
	var totalBetOnTeam2 int32

	for _, bet := range bets {
		switch bet.TeamPos {
		case 1:
			totalBetOnTeam1 += bet.Amount
		case 2:
			totalBetOnTeam2 += bet.Amount
		}
	}

	totalBets := totalBetOnTeam1 + totalBetOnTeam2

	return &pb.CalculateOddsResponse{
		OddsTeam1: float64(totalBets) / float64(totalBetOnTeam1),
		OddsTeam2: float64(totalBets) / float64(totalBetOnTeam2),
	}, nil
}

// Helper function to create a confirmation response with an error.
func confirmError(err error) (*pb.Confirmation, error) {
	return &pb.Confirmation{
		Success: false,
		Message: err.Error(),
	}, err
}
