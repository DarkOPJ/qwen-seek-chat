<template>
  <div class="max-w-3xl mx-auto mt-24 flex flex-col items-center text-center">
    <svg class="w-24 h-24 mb-8 neural-glow brightness-125" viewBox="0 0 32 32" fill="none" aria-hidden="true">
      <rect width="32" height="32" rx="8" fill="#000"/>
      <path d="M8 16C8 11.5817 11.5817 8 16 8C20.4183 8 24 11.5817 24 16C24 20.4183 20.4183 24 16 24C11.5817 24 8 20.4183 8 16Z" stroke="#A855F7" stroke-width="2"/>
      <path d="M16 8V16L21 19" stroke="#A855F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <h2 class="font-h3 text-h3 md:text-h2 mb-4 text-white">Precision Intelligence.</h2>
    <p class="font-body-lg text-body-lg text-on-secondary-container mb-12 max-w-xl">
      Design architectures, debug production logic, or orchestrate complex data flows with Qwen Chat's unified workspace.
    </p>

    <!-- Prompt Suggestions Bento -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
      <SuggestionCard
        v-for="prompt in prompts"
        :key="prompt.title"
        :prompt="prompt"
        @click="$emit('use-prompt', prompt.content)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SuggestionCard from './SuggestionCard.vue'

const props = defineProps({})
const emit = defineEmits(['use-prompt'])

const prompts = ref([
  { icon: 'code', title: 'Refactor React Component', desc: 'Optimize a legacy class component for React 18 hooks and performance.', content: 'Refactor this React class component to use hooks and modern patterns:\n```jsx\nclass UserProfile extends React.Component {\n  state = { user: null, loading: true }\n  async componentDidMount() {\n    const user = await fetchUser(this.props.userId)\n    this.setState({ user, loading: false })\n  }\n  render() {\n    if (this.state.loading) return <div>Loading...</div>\n    return <div>{this.state.user.name}</div>\n  }\n}\n```' },
  { icon: 'schema', title: 'SQL Query Optimization', desc: 'Analyze a complex JOIN query for potential indexing improvements.', content: 'Analyze this SQL query for optimization opportunities:\n```sql\nSELECT u.*, p.title, p.body\nFROM users u\nJOIN posts p ON u.id = p.user_id\nJOIN comments c ON p.id = c.post_id\nWHERE u.created_at > \'2024-01-01\'\nAND p.published = true\nGROUP BY u.id, p.id\nHAVING COUNT(c.id) > 5\nORDER BY u.created_at DESC\n```' },
  { icon: 'terminal', title: 'CI/CD Pipeline Design', desc: 'Create a Github Action workflow for automated testing and staging deployment.', content: 'Create a GitHub Actions workflow that:\n1. Runs on push to main and PRs\n2. Sets up Node.js 20\n3. Installs dependencies with npm ci\n4. Runs linting and type checking\n5. Runs unit tests with coverage\n6. Deploys to staging on main branch\n7. Uses environments for protection rules' },
  { icon: 'auto_awesome', title: 'Creative Brand Strategy', desc: 'Brainstorm names and visual identity directions for a new AI startup.', content: 'Help me brainstorm for a new AI startup that provides:\n- Local-first AI inference\n- Privacy-focused\n- Developer tools\n\nProvide:\n1. 10 name ideas with rationale\n2. Visual identity directions (3 concepts)\n3. Tagline options\n4. Brand voice guidelines' }
])
</script>

<style scoped>
/* Scoped styles if needed */
</style>