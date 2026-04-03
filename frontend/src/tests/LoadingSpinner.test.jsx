import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import LoadingSpinner from '../components/common/LoadingSpinner'

describe('LoadingSpinner', () => {
  it('renders with default message', () => {
    render(<LoadingSpinner />)
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('renders with custom message', () => {
    render(<LoadingSpinner message="Fetching data..." />)
    expect(screen.getByText('Fetching data...')).toBeInTheDocument()
  })

  it('has role=status for accessibility', () => {
    render(<LoadingSpinner message="Please wait" />)
    expect(screen.getByRole('status')).toBeInTheDocument()
  })

  it('aria-label matches the message', () => {
    render(<LoadingSpinner message="Loading graph..." />)
    expect(screen.getByRole('status')).toHaveAttribute('aria-label', 'Loading graph...')
  })
})
