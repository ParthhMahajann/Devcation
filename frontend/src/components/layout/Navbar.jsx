import { Link, useLocation } from 'react-router-dom'

const NAV_LINKS = [
  { to: '/',             label: 'Dashboard'   },
  { to: '/diagnose',     label: 'Diagnose'    },
  { to: '/interactions', label: 'Drugs'       },
  { to: '/explore',      label: 'Explorer'    },
  { to: '/patients',     label: 'Patients'    },
]

export default function Navbar() {
  const { pathname } = useLocation()
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur border-b border-slate-700/50">
      <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-14">
        <Link to="/" className="flex items-center gap-2 text-white font-bold text-lg">
          <span className="text-sky-400">🧠</span>
          <span>MedGraph <span className="text-sky-400">AI</span></span>
        </Link>
        <div className="flex items-center gap-1" role="list">
          {NAV_LINKS.map(({ to, label }) => (
            <Link
              key={to}
              to={to}
              role="listitem"
              aria-current={pathname === to ? 'page' : undefined}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400 ${
                pathname === to
                  ? 'bg-sky-600 text-white'
                  : 'text-slate-400 hover:text-white hover:bg-slate-700'
              }`}
            >
              {label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  )
}
