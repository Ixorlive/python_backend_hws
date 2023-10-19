package mongodb

import (
	"context"

	"Match/domain"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type MatchRepository struct {
	client *mongo.Client
	db     *mongo.Database
}

// NewMatchRepository creates a new MongoDB MatchRepository.
func NewMatchRepository(mongoURI string, dbName string) (*MatchRepository, error) {
	clientOptions := options.Client().ApplyURI(mongoURI)
	client, err := mongo.Connect(context.Background(), clientOptions)
	if err != nil {
		return nil, err
	}

	db := client.Database(dbName)
	return &MatchRepository{client: client, db: db}, nil
}

func (repo *MatchRepository) AddMatch(ctx context.Context, m domain.Match) (domain.Match, error) {
	collection := repo.db.Collection("matches")
	m.ID = primitive.NewObjectID().Hex() // Generate a new MongoDB ObjectID
	_, err := collection.InsertOne(ctx, m)
	if err != nil {
		return domain.Match{}, err
	}
	return m, nil
}

func (repo *MatchRepository) UpdateMatchTime(ctx context.Context, id string, newTime string) (domain.Match, error) {
	collection := repo.db.Collection("matches")
	objID, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return domain.Match{}, err
	}

	filter := bson.M{"_id": objID}
	update := bson.M{"$set": bson.M{"match_time": newTime}}

	res := collection.FindOneAndUpdate(ctx, filter, update)
	if res.Err() != nil {
		return domain.Match{}, res.Err()
	}

	var updatedMatch domain.Match
	if err := res.Decode(&updatedMatch); err != nil {
		return domain.Match{}, err
	}

	return updatedMatch, nil
}

func (repo *MatchRepository) MarkMatchAsCompleted(ctx context.Context, id string) (domain.Match, error) {
	collection := repo.db.Collection("matches")
	objID, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return domain.Match{}, err
	}

	filter := bson.M{"_id": objID}
	update := bson.M{"$set": bson.M{"status": domain.Completed}}

	res := collection.FindOneAndUpdate(ctx, filter, update)
	if res.Err() != nil {
		return domain.Match{}, res.Err()
	}

	var updatedMatch domain.Match
	if err := res.Decode(&updatedMatch); err != nil {
		return domain.Match{}, err
	}

	return updatedMatch, nil
}

func (repo *MatchRepository) ListMatches(ctx context.Context, status domain.MatchStatus) ([]domain.Match, error) {
	collection := repo.db.Collection("matches")
	filter := bson.M{"status": status}

	cur, err := collection.Find(ctx, filter)
	if err != nil {
		return nil, err
	}
	defer cur.Close(ctx)

	var matches []domain.Match
	for cur.Next(ctx) {
		var match domain.Match
		if err := cur.Decode(&match); err != nil {
			return nil, err
		}
		matches = append(matches, match)
	}

	return matches, nil
}
