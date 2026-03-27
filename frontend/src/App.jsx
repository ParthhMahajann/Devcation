import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/layout/Navbar'
import Dashboard from './pages/Dashboard'
import DiagnosePage from './pages/DiagnosePage'
import DrugInteractionsPage from './pages/DrugInteractionsPage'
import GraphExplorerPage from './pages/GraphExplorerPage'
import PatientPage from './pages/PatientPage'

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-900 text-slate-100">
        <Navbar />
        <main className="pt-14">
          <Routes>
            <Route path="/"             element={<Dashboard />}           />
            <Route path="/diagnose"     element={<DiagnosePage />}        />
            <Route path="/interactions" element={<DrugInteractionsPage />} />
            <Route path="/explore"      element={<GraphExplorerPage />}   />
            <Route path="/patients"     element={<PatientPage />}         />
            <Route path="*"             element={<NotFound />}            />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center h-[60vh] text-center">
      <div className="text-6xl mb-4">404</div>
      <h1 className="text-2xl font-bold text-white mb-2">Page not found</h1>
      <a href="/" className="text-sky-400 hover:underline">Go home</a>
    </div>
  )
}
