import { createContext, useContext, useState, useEffect } from "react";

interface AuthContextType {
  isLoggedIn: boolean;
  userEmail: string | null;
  login: (email: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("session_token")
  );
  const [userEmail, setUserEmail] = useState<string | null>(
    localStorage.getItem("user_email") || null
  );

  const login = (email: string) => {
    localStorage.setItem("user_email", email);
    setUserEmail(email);
    setIsLoggedIn(true);
  };

  const logout = () => {
    localStorage.removeItem("session_token");
    localStorage.removeItem("user_email");
    localStorage.removeItem("id");
    localStorage.removeItem("has_onboarded");
    setUserEmail(null);
    setIsLoggedIn(false);
  };

  useEffect(() => {
    // Keep email synced on reload
    if (!userEmail && localStorage.getItem("user_email")) {
      setUserEmail(localStorage.getItem("user_email"));
    }
  }, []);

  return (
    <AuthContext.Provider value={{ isLoggedIn, userEmail, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
};
