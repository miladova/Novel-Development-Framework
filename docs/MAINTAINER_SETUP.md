# Public repository maintenance

The framework is intended for public reuse. Keep its MIT license and story-neutral scope intact.

In GitHub Settings -> General, enable **Template repository** to expose the one-click template workflow. Repository visibility and template status are host settings, not effects of the Markdown files. See [GitHub's template setup guide](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository).

Suggested topics: creative-writing, novel-writing, worldbuilding, storytelling, writing-tools, ai-assisted, canon-management, repository-template.

Confirm GitHub Actions runs the validation workflow. The workflow uses read-only contents permissions and pinned action commits. Do not give it secrets or write permission merely to make a failing check pass. Dependency updates are proposed for human review.

Consider branch protections, required reviews, and private vulnerability reporting as the contributor community grows. These settings are not configured by copying this framework. No automated merge or release workflow is included.

Before a release, run the test suite and structural validator, inspect all tracked files for private or story-specific data, verify documentation against actual capabilities, and record changes in the changelog. Create a tag or GitHub release only through an explicitly authorized release task.
