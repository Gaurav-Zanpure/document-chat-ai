type Source = {
  document_name: string;
  page: number;
  chunk_index: number;
  text: string;
};

type SourceListProps = {
  sources: Source[];
};

export default function SourceList({ sources }: SourceListProps) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-6 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      <h3 className="mb-4 text-lg font-semibold text-gray-900">Sources</h3>

      <div className="space-y-4">
        {sources.map((source, index) => (
          <div
            key={index}
            className="rounded-xl border border-gray-200 bg-gray-50 p-4"
          >
            <p className="mb-2 text-sm font-medium text-gray-900">
              {source.document_name} • Page {source.page} • Chunk {source.chunk_index}
            </p>
            <p className="text-sm leading-6 text-gray-700">{source.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}