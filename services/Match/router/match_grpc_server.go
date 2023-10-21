package router

import (
	"Match/domain"
	pb "Match/proto_gen/matchservicepb"
	"context"
)

type MatchGRPCServer struct {
	repo domain.MatchRepository
	pb.UnimplementedMatchServiceServer
}

func NewMatchGRPCServer(r domain.MatchRepository) *MatchGRPCServer {
	return &MatchGRPCServer{repo: r}
}

func (s *MatchGRPCServer) AddMatch(ctx context.Context, req *pb.AddMatchRequest) (*pb.MatchResponse, error) {
	match := domain.Match{
		Team1:     req.GetTeam1(),
		Team2:     req.GetTeam2(),
		MatchTime: req.GetMatchTime(),
		Status:    domain.Upcoming, // assuming the default status for a new match is 'Upcoming'
	}

	storedMatch, err := s.repo.AddMatch(ctx, match)
	if err != nil {
		return nil, err
	}

	return &pb.MatchResponse{Match: convertDomainMatchToProto(storedMatch)}, nil
}

func (s *MatchGRPCServer) UpdateMatchTime(ctx context.Context, req *pb.UpdateMatchTimeRequest) (*pb.MatchResponse, error) {
	storedMatch, err := s.repo.UpdateMatchTime(ctx, req.GetId(), req.GetNewTime())
	if err != nil {
		return nil, err
	}

	return &pb.MatchResponse{Match: convertDomainMatchToProto(storedMatch)}, nil
}

func (s *MatchGRPCServer) MarkMatchAsCompleted(ctx context.Context, req *pb.MarkMatchRequest) (*pb.MatchResponse, error) {
	storedMatch, err := s.repo.MarkMatchAsCompleted(ctx, req.GetId())
	if err != nil {
		return nil, err
	}

	return &pb.MatchResponse{Match: convertDomainMatchToProto(storedMatch)}, nil
}

// Convert single domain.Match to protobuf Match
func convertDomainMatchToProto(m domain.Match) *pb.Match {
	return &pb.Match{
		Id:        m.ID,
		Team1:     m.Team1,
		Team2:     m.Team2,
		MatchTime: m.MatchTime,
		Status:    pb.MatchStatus(m.Status),
	}
}

func (s *MatchGRPCServer) ListMatches(ctx context.Context, req *pb.ListMatchesRequest) (*pb.ListMatchesResponse, error) {
	matches, err := s.repo.ListMatches(ctx, domain.MatchStatus(req.GetStatusFilter()))
	if err != nil {
		return nil, err
	}

	pbMatches := make([]*pb.Match, 0, len(matches))
	for _, m := range matches {
		pbMatches = append(pbMatches, convertDomainMatchToProto(m))
	}

	return &pb.ListMatchesResponse{Matches: pbMatches}, nil
}
