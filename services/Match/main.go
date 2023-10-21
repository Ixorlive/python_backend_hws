package main

import (
	"log"
	"net"

	"Match/infras/mongodb"
	pb "Match/proto_gen/matchservicepb"
	"Match/router"

	"google.golang.org/grpc"
)

const (
	CONNECTION_STRING = "mongodb://ixor:ixor@localhost:27017/"
	DATABASE_NAME     = "bookmaker_db"
	GRPC_PORT         = ":50052"
)

func main() {
	matchRepo, err := mongodb.NewMatchRepository(CONNECTION_STRING, DATABASE_NAME)

	if err != nil {
		log.Fatalf("Failed to connect to MongoDB: %v", err)
	}

	// Create and run gRPC server
	grpcServer := grpc.NewServer()
	matchServer := router.NewMatchGRPCServer(matchRepo)
	pb.RegisterMatchServiceServer(grpcServer, matchServer)

	listener, err := net.Listen("tcp", GRPC_PORT)
	if err != nil {
		log.Fatalf("Failed to listen on port %v: %v", GRPC_PORT, err)
	}
	log.Printf("Starting gRPC server on port %v...", GRPC_PORT)

	if err := grpcServer.Serve(listener); err != nil {
		log.Fatalf("Failed to serve gRPC server: %v", err)
	}
}
