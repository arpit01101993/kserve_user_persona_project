# User Persona Recommendation with Airflow + KServe

✅ This example shows:
- Airflow DAG that calls your KServe REST API for real-time inference
- KServe InferenceService YAML for scikit-learn model
- Kubernetes Secret for S3 credentials

## Deploy

1. Create secret:
   kubectl apply -f s3_secret.yaml

2. Deploy InferenceService:
   kubectl apply -f inferenceservice.yaml

3. Test KServe endpoint:
   curl -X POST http://<endpoint>/v1/models/user-persona-recommender:predict -d '{"instances": [[0.5, 1.2, 3.4, 1, 0, 1]]}'

## Airflow DAG
See `airflow/call_kserve_dag.py` to run predictions from Airflow.
