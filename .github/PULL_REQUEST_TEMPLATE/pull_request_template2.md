# Pull Request Template

## Description

provide a comprehensive summary of the changes introduced in this pull request. include details about the modifications made, the purpose behind these changes, and how they address the issue referenced below. additionally, outline any dependencies that are essential for these changes to function correctly.

closes # (issue number)

## Change Category

select the most appropriate category for this change. Remove any irrelevant options.

- [ ] bug fix: a non-breaking change that resolves an identified issue
- [ ] new feature: a non-breaking addition of functionality
- [ ] breaking change: a modification that alters existing functionality
- [ ] documentation update: changes that necessitate an update to the project's documentation

## Testing and Validation

describe the testing procedures undertaken to ensure the integrity and effectiveness of the implemented changes. provide clear instructions for reproducing these tests

### Test Configuration:
- firmware version:
- hardware info:
- toolchain used:
- SDK info:

## Review Checklist

before submitting this pr ensure that all items in the checklist have been addressed:

- [ ] abided to the project's coding standards and conventions
- [ ] conducted a thorough self-review of the code
- [ ] included comments throughout the code, especially in complex sections, for better readability
- [ ] updated the documentation to reflect the changes made
- [ ] ensured that the changes do not introduce new warnings or errors
- [ ] added tests to validate the effectiveness of the changes
- [ ] verified that both new and existing unit tests pass locally with the changes applied
- [ ] addresed any dependencies by merging and publishing changes in relevant downstream modules
- [ ] agreed to license the contribution under the [MIT License](https://github.com/NoGambling1/ConsoleGames/LICENSE).
- [ ] acknowledged that contributions may be altered or rejected

## Additional Notes

if there are any additional considerations or notes that reviewers should be aware of, please detail them here.