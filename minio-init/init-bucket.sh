#!/bin/bash

# Wait for MinIO to be ready
sleep 10

# Create the documents bucket
mc alias set myminio http://localhost:9000 minioadmin minioadmin123
mc mb myminio/documents --ignore-existing

echo "MinIO bucket 'documents' created successfully!" 