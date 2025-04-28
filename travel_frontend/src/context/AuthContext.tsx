import { createContext, useContext, useState, useEffect } from "react";

interface AuthContextType {
  isLoggedIn: boolean;
  userEmail: string | null;
  userId: number | null;
  hasOnboarded: boolean;
  login: (email: string, id: number) => void;
  logout: () => void;
  setHasOnboarded: (value: boolean) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("session_token")
  );
  const [userEmail, setUserEmail] = useState<string | null>(
    localStorage.getItem("user_email") || null
  );
  const [userId, setUserId] = useState<number | null>(
    localStorage.getItem("id") ? parseInt(localStorage.getItem("id")!) : null
  );
  const [hasOnboarded, setHasOnboarded] = useState<boolean>(
    localStorage.getItem("has_onboarded") === "true"
  );

  const login = (email: string, id: number) => {
    localStorage.setItem("user_email", email);
    localStorage.setItem("id", id.toString());
    setUserEmail(email);
    setUserId(id);
    setIsLoggedIn(true);
  };

  const logout = () => {
    localStorage.removeItem("session_token");
    localStorage.removeItem("user_email");
    localStorage.removeItem("id");
    localStorage.removeItem("has_onboarded");
    setUserEmail(null);
    setUserId(null);
    setHasOnboarded(false);
    setIsLoggedIn(false);
  };

  useEffect(() => {
    if (!userEmail && localStorage.getItem("user_email")) {
      setUserEmail(localStorage.getItem("user_email"));
    }
    if (!userId && localStorage.getItem("id")) {
      setUserId(parseInt(localStorage.getItem("id")!));
    }
    if (!hasOnboarded && localStorage.getItem("has_onboarded") === "true") {
      setHasOnboarded(true);
    }
  }, []);

  return (
    <AuthContext.Provider
      value={{
        isLoggedIn,
        userEmail,
        userId,
        hasOnboarded,
        login,
        logout,
        setHasOnboarded,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
};
