package mongodb

import (
	"Bets/domain"
	"context"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type BetsRepository struct {
	client *mongo.Client
	db     *mongo.Database
}

func NewBetsRepository(mongoURI string, dbName string) (*BetsRepository, error) {
	clientOptions := options.Client().ApplyURI(mongoURI)
	client, err := mongo.Connect(context.Background(), clientOptions)
	if err != nil {
		return nil, err
	}

	db := client.Database(dbName)
	return &BetsRepository{client: client, db: db}, nil
}

func (r *BetsRepository) Place(ctx context.Context, b domain.Bet) error {
	collection := r.db.Collection("bets")
	_, err := collection.InsertOne(ctx, b)
	if err != nil {
		return err
	}
	return nil
}

func (r *BetsRepository) AllBetsOnMatch(ctx context.Context, matchID string) ([]domain.Bet, error) {
	collection := r.db.Collection("bets")
	filter := bson.M{"matchid": matchID} // Match on the "MatchID" field in MongoDB.

	cur, err := collection.Find(ctx, filter)
	if err != nil {
		return nil, err
	}
	defer cur.Close(ctx)

	var bets []domain.Bet
	for cur.Next(ctx) {
		var bet domain.Bet
		err := cur.Decode(&bet)
		if err != nil {
			return nil, err
		}
		bets = append(bets, bet)
	}

	if err := cur.Err(); err != nil {
		return nil, err
	}

	return bets, nil
}
