export interface DocumentSummary {
  filename: string;
  file_size_bytes: number;
  paragraph_count: number;
  non_empty_paragraphs: number;
  table_count: number;
  image_count: number;
  total_words: number;
  total_chars: number;
  estimated_pages: number;
  is_empty: boolean;
}

export interface ClassificationItem {
  paragraph_index: number;
  text: string;
  clean_text: string;
  final_class: string;
  confidence: number;
  confidence_percent: number;
  ml_class: string;
  ml_confidence: number;
  rule_class: string | null;
  rule_confidence: number | null;
  rule_applied: boolean;
  decision_source: string;
  reason: string;
  original_style: string;
  original_font_size: number | null;
  original_bold: boolean;
  original_italic: boolean;
  original_alignment: string;
}

export interface AnalysisResponse {
  summary: DocumentSummary;
  class_distribution: Record<string, number>;
  classifications: ClassificationItem[];
}

export interface FormattingStats {
  output_path: string;
  output_filename?: string;
  paragraphs_formatted: number;
  tables_formatted: number;
  style_distribution: Record<string, number>;
  toc_included: boolean;
  file_size_bytes: number;
  elapsed_time_seconds: number;
}

export interface BenchmarkScaleResult {
  page_scale: number;
  paragraphs_processed: number;
  tables_processed: number;
  figures_processed: number;
  elapsed_time_seconds: number;
  throughput_paragraphs_per_sec: number;
  peak_memory_mb: number;
  memory_delta_mb: number;
  detected_structures: Record<string, number>;
}

export interface BenchmarkSuite {
  timestamp: string;
  scales_tested: number[];
  results: BenchmarkScaleResult[];
  system_info: {
    python_version: string;
    cpu_count: number;
    total_physical_memory_mb: number;
  };
}

export interface PublicationSpecs {
  top_margin_cm: number;
  bottom_margin_cm: number;
  left_margin_cm: number;
  right_margin_cm: number;
  body_font_name: string;
  body_font_size: number;
  body_line_spacing: number;
  first_line_indent_cm: number;
  include_toc: boolean;
}
