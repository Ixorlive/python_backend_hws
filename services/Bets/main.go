package main

import (
	"Bets/client"
	"Bets/infras/mongodb"
	"Bets/router"
	"log"
	"net"

	pb "Bets/proto_gen/betservicepb"

	"google.golang.org/grpc"
)

const (
	// config
	CONNECTION_STRING      = "mongodb://ixor:ixor@localhost:27017/"
	DATABASE_NAME          = "bookmaker_db"
	IDENTITY_CLIEN_ADDRESS = "localhost:50051"
	GRPC_PORT              = ":50053"

	// errors msg
	MONGODB_CONNECT_ERR  = "Failed to connect to MongoDB: %v"
	IDENTITY_SERVICE_ERR = "Failed to connect to Identity service: %v"
	GRPC_LISTEN_ERR      = "Failed to listen on port %v: %v"
	GRPC_SERVE_ERR       = "Failed to serve gRPC server: %v"

	GRPC_START_MSG = "Starting gRPC server on port %v..."
)

func main() {
	betRepo, err := mongodb.NewBetsRepository(CONNECTION_STRING, DATABASE_NAME)

	if err != nil {
		log.Fatalf(MONGODB_CONNECT_ERR, err)
	}

	identityClient, err := client.NewIdentityClient(IDENTITY_CLIEN_ADDRESS)

	if err != nil {
		log.Fatalf(IDENTITY_SERVICE_ERR, err)
	}

	grpcServer := grpc.NewServer()
	betServer := router.NewBetGRPCServer(betRepo, identityClient)
	pb.RegisterBetsServer(grpcServer, betServer)

	listener, err := net.Listen("tcp", GRPC_PORT)
	if err != nil {
		log.Fatalf(GRPC_LISTEN_ERR, GRPC_PORT, err)
	}

	log.Printf(GRPC_START_MSG, GRPC_PORT)

	if err := grpcServer.Serve(listener); err != nil {
		log.Fatalf(GRPC_SERVE_ERR, err)
	}
}
