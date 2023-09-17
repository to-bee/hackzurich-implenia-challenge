openapi-generator generate \
  -i http://127.0.0.1:8000/openapi.json \
  -g typescript-angular \
  -o ./src/openapi-generated \
  --global-property skipFormModel=false \
  --additional-properties io.swagger.v3.parser.util.RemoteUrl.trustAll=true,useSingleRequestParameter=true,modelPropertyNaming=original,stringEnums=true,supportsES6=true,withInterfaces=true \
  --skip-validate-spec \
  --package-name=openapi-generated
