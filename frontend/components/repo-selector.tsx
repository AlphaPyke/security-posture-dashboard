import { GitBranch } from "lucide-react";

type RepositoryOption = {
  id: string;
  fullName: string;
  visibility: "public" | "private";
};

export function RepoSelector({
  repositories,
  selectedId
}: Readonly<{ repositories: RepositoryOption[]; selectedId: string }>) {
  return (
    <label className="flex min-w-72 items-center gap-2 text-sm">
      <GitBranch className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
      <span className="sr-only">Repository</span>
      <select
        className="h-10 w-full rounded-md border-border bg-white text-sm shadow-sm focus:border-primary focus:ring-primary"
        defaultValue={selectedId}
      >
        {repositories.map((repo) => (
          <option key={repo.id} value={repo.id}>
            {repo.fullName} ({repo.visibility})
          </option>
        ))}
      </select>
    </label>
  );
}
