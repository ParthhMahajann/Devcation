import { Component } from 'react'

export default class ErrorBoundary extends Component {
  state = { hasError: false, error: null }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex flex-col items-center justify-center py-16 gap-4 text-center">
          <div className="text-5xl">⚠️</div>
          <h2 className="text-xl font-semibold text-red-400">Something went wrong</h2>
          <p className="text-slate-400 text-sm max-w-md">{this.state.error?.message}</p>
          <button
            onClick={() => this.setState({ hasError: false })}
            className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg text-sm"
          >
            Try again
          </button>
        </div>
      )
    }
    return this.props.children
  }
}
