type StatusCardProps = {
  documentsLoaded: number;
  chunksIndexed: number;
  lastUploadedDocument: string;
  status: string;
};

export default function StatusCard({
  documentsLoaded,
  chunksIndexed,
  lastUploadedDocument,
  status,
}: StatusCardProps) {
  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-xl font-semibold text-gray-900">Knowledge Base Status</h2>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="rounded-xl bg-gray-50 p-4">
          <p className="text-sm text-gray-500">Documents Loaded</p>
          <p className="mt-1 text-2xl font-semibold text-gray-900">{documentsLoaded}</p>
        </div>

        <div className="rounded-xl bg-gray-50 p-4">
          <p className="text-sm text-gray-500">Chunks Indexed</p>
          <p className="mt-1 text-2xl font-semibold text-gray-900">{chunksIndexed}</p>
        </div>

        <div className="rounded-xl bg-gray-50 p-4 sm:col-span-2">
          <p className="text-sm text-gray-500">Last Uploaded Document</p>
          <p className="mt-1 text-base font-medium text-gray-900 break-all">
            {lastUploadedDocument || "No document uploaded yet"}
          </p>
        </div>

        <div className="rounded-xl bg-gray-50 p-4 sm:col-span-2">
          <p className="text-sm text-gray-500">System Status</p>
          <p className="mt-1 text-base font-medium text-green-700">{status}</p>
        </div>
      </div>
    </div>
  );
}