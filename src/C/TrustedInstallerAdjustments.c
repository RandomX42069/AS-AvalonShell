#include <windows.h>
#include <tlhelp32.h>
#include <stdio.h>

/* Enable a named privilege (ANSI version) */
BOOL EnablePrivilege(LPCSTR privName) {
    HANDLE hToken = NULL;
    TOKEN_PRIVILEGES tp;
    LUID luid;

    if (!OpenProcessToken(GetCurrentProcess(),
                          TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY,
                          &hToken)) {
        printf("OpenProcessToken failed: %lu\n", GetLastError());
        return FALSE;
    }

    if (!LookupPrivilegeValueA(NULL, privName, &luid)) {
        printf("LookupPrivilegeValueA(%s) failed: %lu\n", privName, GetLastError());
        CloseHandle(hToken);
        return FALSE;
    }

    tp.PrivilegeCount = 1;
    tp.Privileges[0].Luid = luid;
    tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;

    if (!AdjustTokenPrivileges(hToken, FALSE, &tp, sizeof(tp), NULL, NULL)) {
        printf("AdjustTokenPrivileges failed: %lu\n", GetLastError());
        CloseHandle(hToken);
        return FALSE;
    }

    if (GetLastError() == ERROR_NOT_ALL_ASSIGNED) {
        printf("Privilege %s not assigned to token.\n", privName);
        CloseHandle(hToken);
        return FALSE;
    }

    CloseHandle(hToken);
    return TRUE;
}

/* Find a running process by exe name (Unicode version) */
__declspec(dllexport) DWORD FindProcessID(const wchar_t *processName) {
    PROCESSENTRY32W pe32;
    pe32.dwSize = sizeof(PROCESSENTRY32W);

    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hSnapshot == INVALID_HANDLE_VALUE) return 0;

    if (Process32FirstW(hSnapshot, &pe32)) {
        do {
            if (_wcsicmp(pe32.szExeFile, processName) == 0) {
                DWORD pid = pe32.th32ProcessID;
                CloseHandle(hSnapshot);
                return pid;
            }
        } while (Process32NextW(hSnapshot, &pe32));
    }

    CloseHandle(hSnapshot);
    return 0;
}

/* Spawn a process as TrustedInstaller */
__declspec(dllexport) BOOL RunAsTrustedInstaller(LPCWSTR applicationPath, LPCWSTR commandLineArgs) {
    DWORD tiPid = 0;
    HANDLE hProc = NULL, hProcToken = NULL, hDupToken = NULL;
    STARTUPINFOW si;
    PROCESS_INFORMATION pi;

    // Enable required privileges
    if (!EnablePrivilege(SE_DEBUG_NAME)) return FALSE;
    if (!EnablePrivilege(SE_IMPERSONATE_NAME)) return FALSE;
    if (!EnablePrivilege(SE_ASSIGNPRIMARYTOKEN_NAME)) return FALSE;
    if (!EnablePrivilege(SE_INCREASE_QUOTA_NAME)) return FALSE;

    tiPid = FindProcessID(L"TrustedInstaller.exe");
    if (tiPid == 0) return FALSE;

    // Open TrustedInstaller process with sufficient rights
    hProc = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_CREATE_PROCESS | PROCESS_DUP_HANDLE, FALSE, tiPid);
    if (!hProc) return FALSE;

    // Open and duplicate token
    if (!OpenProcessToken(hProc,
                          TOKEN_DUPLICATE | TOKEN_ASSIGN_PRIMARY | TOKEN_QUERY |
                          TOKEN_ADJUST_DEFAULT | TOKEN_ADJUST_SESSIONID | TOKEN_ADJUST_PRIVILEGES,
                          &hProcToken)) {
        CloseHandle(hProc);
        return FALSE;
    }

    if (!DuplicateTokenEx(hProcToken,
                          TOKEN_ALL_ACCESS,
                          NULL,
                          SecurityImpersonation,
                          TokenPrimary,
                          &hDupToken)) {
        CloseHandle(hProcToken);
        CloseHandle(hProc);
        return FALSE;
    }

    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    // Prepare writable command line buffer
    wchar_t cmdBuffer[32768]; // Large enough for typical command lines
    if (commandLineArgs) {
        wcsncpy(cmdBuffer, commandLineArgs, _countof(cmdBuffer) - 1);
        cmdBuffer[_countof(cmdBuffer) - 1] = L'\0';
    } else {
        cmdBuffer[0] = L'\0';
    }

    BOOL ok = CreateProcessWithTokenW(
        hDupToken,
        LOGON_WITH_PROFILE,
        applicationPath,   // Full exe path
        cmdBuffer,         // Arguments (writable)
        CREATE_NEW_CONSOLE,
        NULL,
        NULL,
        &si,
        &pi
    );

    if (ok) {
        CloseHandle(pi.hThread);
        CloseHandle(pi.hProcess);
    }

    CloseHandle(hDupToken);
    CloseHandle(hProcToken);
    CloseHandle(hProc);

    return ok;
}
