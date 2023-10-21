package client

import (
	"Bets/domain"
	"context"
	"errors"
	"fmt"

	pb "Bets/proto_gen/identityservicepb"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type IdentityClient struct {
	conn   *grpc.ClientConn
	client pb.UserAuthClient
}

func NewIdentityClient(serverAddress string) (*IdentityClient, error) {
	conn, err := grpc.Dial(serverAddress, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return nil, fmt.Errorf("failed to dial Identity server: %v", err)
	}

	client := pb.NewUserAuthClient(conn)
	return &IdentityClient{conn: conn, client: client}, nil
}

func (c *IdentityClient) Withdraw(ctx context.Context, d domain.Debit) error {
	req := &pb.Transaction{Login: d.Login, Amount: d.Amount}
	conf, err := c.client.Withdraw(ctx, req)
	if conf.GetSuccess() {
		return nil
	}
	if err == nil {
		return errors.New(conf.GetMessage())
	}
	return err
}

func (c *IdentityClient) Close() error {
	return c.conn.Close()
}
