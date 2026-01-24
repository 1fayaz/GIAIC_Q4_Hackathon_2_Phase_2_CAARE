---
name: frontend-skill
description: Build frontend pages, reusable components, layouts, and styling using modern UI best practices.
---

# Frontend Skill – Pages, Components & Styling

## Instructions

1. **Page Construction**
   - Build pages using a clear structure
   - Separate layout, content, and logic
   - Handle loading, error, and empty states
   - Ensure pages are responsive across devices

2. **Component Design**
   - Create reusable, composable components
   - Keep components small and focused
   - Use clear props and predictable behavior
   - Avoid unnecessary re-renders

3. **Layout System**
   - Use consistent layout patterns
   - Apply grid and flexbox effectively
   - Maintain visual hierarchy and spacing
   - Support responsive breakpoints

4. **Styling**
   - Use a consistent styling system (CSS Modules, Tailwind, styled-components, etc.)
   - Follow design tokens for colors, spacing, and typography
   - Ensure accessible contrast and font sizes
   - Avoid inline styles unless necessary

## Best Practices
- Mobile-first and responsive design
- Consistent naming conventions
- Accessibility (semantic HTML, ARIA when needed)
- Reuse components instead of duplicating UI
- Keep styles maintainable and scalable
- Optimize assets and fonts for performance

## Example Structure
```tsx
// Page
<PageLayout>
  <Header />
  <MainContent>
    <Card title="Feature">
      <Button>Get Started</Button>
    </Card>
  </MainContent>
</PageLayout>
