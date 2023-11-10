import { useState, createContext } from "react"

export const AppContext = createContext(null)

export function AppContextProvider({ children }) {
    const [folderPath, setFolderPath] = useState('')
    return (
        <AppContext.Provider 
            value={{
                folderPath,
                setFolderPath
            }}
        >
            {children}
        </AppContext.Provider>
    )
}