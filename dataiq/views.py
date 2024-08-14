from django.views.decorators.csrf import csrf_exempt

import numpy as np
import torch
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoModel, AutoTokenizer

from .models import Chunk


class ChunkSearchAPIView(APIView):
    class ChunkSerializer(serializers.ModelSerializer):
        class Meta:
            model = Chunk
            fields = ["id", "text", "url", "keywords"]

    def post(self, request, format=None):
        query = request.data.get("query", "")
        if not query:
            return Response(
                {"error": "Query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tokenizer = AutoTokenizer.from_pretrained("intfloat/multilingual-e5-large")
        model = AutoModel.from_pretrained("intfloat/multilingual-e5-large")

        def embed_text(text):
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                embeddings = model(**inputs).last_hidden_state.mean(dim=1)
            return embeddings.numpy().reshape(1, -1)

        query_embedding = embed_text(query)

        chunks = list(Chunk.objects.all())
        embeddings = np.vstack(
            [self.retrieve_chunk_embedding(chunk) for chunk in chunks]
        )

        if query_embedding.shape[1] != embeddings.shape[1]:
            return Response(
                {"error": "Embedding dimensions do not match"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        similarities = cosine_similarity(query_embedding, embeddings)[0]
        top_indices = similarities.argsort()[-5:][::-1]

        top_indices = list(map(int, top_indices))

        top_chunks = [chunks[i] for i in top_indices]
        serializer = self.ChunkSerializer(top_chunks, many=True)
        return Response(serializer.data)

    def retrieve_chunk_embedding(self, chunk):
        expected_size = 1024
        embedding = np.frombuffer(chunk.embedding, dtype=np.float32)

        if embedding.size != expected_size:
            raise ValueError("Embedding size does not match expected size.")

        return embedding.reshape(1, -1)
