# Multi-stage build for IntelliFormat - Offline ML-Based DOCX Publication Formatter
FROM node:20-alpine AS builder

# Install Python and build dependencies
RUN apk add --no-cache python3 py3-pip python3-dev gcc g++ musl-dev

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY requirements-cloud.txt ./

# Install Node dependencies
RUN npm install

# Install Python dependencies using pip with --break-system-packages for Alpine
RUN pip3 install --no-cache-dir --break-system-packages -r requirements-cloud.txt

# Copy application code
COPY . .

# Build the React frontend
RUN npm run build

# Production stage
FROM node:20-alpine

# Install Python runtime and build dependencies for scikit-learn
RUN apk add --no-cache python3 py3-pip python3-dev gcc g++ musl-dev

WORKDIR /app

# Copy Python requirements and install
COPY requirements-cloud.txt ./
RUN pip3 install --no-cache-dir --break-system-packages -r requirements-cloud.txt

# Copy built frontend from builder
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/server.ts ./
COPY --from=builder /app/tsconfig.json ./
COPY --from=builder /app/vite.config.ts ./

# Copy Python application files (excluding GUI for cloud deployment)
COPY --from=builder /app/app.py ./
COPY --from=builder /app/server_api.py ./
COPY --from=builder /app/ml ./ml
COPY --from=builder /app/parser ./parser
COPY --from=builder /app/formatter ./formatter
COPY --from=builder /app/rules ./rules
COPY --from=builder /app/evaluation ./evaluation
COPY --from=builder /app/performance ./performance
COPY --from=builder /app/dataset ./dataset
COPY --from=builder /app/samples ./samples

# Create necessary directories
RUN mkdir -p uploads output

# Build the server
RUN npm run build

# Expose the application port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start the production server
CMD ["npm", "start"]