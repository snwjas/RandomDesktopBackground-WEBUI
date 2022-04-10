#include <windows.h>
//#include <stdio.h>

int main(int argc, char **argv)
{

    // 参数argv：[[name,] command]

    if (argc < 2 || argc > 3)
    {
        return 0;
    }

    char *name = (argc == 2 ? "GlobalRandomDesktopBackgroundShareMemory" : argv[1]);
    char *command = (argc == 2 ? argv[1] : argv[2]);

    HANDLE fmap = OpenFileMapping(FILE_MAP_ALL_ACCESS, -1, name);
    if (fmap == NULL)
    {
        return 0;
    }

    LPVOID fmv = MapViewOfFile(fmap, FILE_MAP_ALL_ACCESS, 0, 0, 0);
    if (fmv != NULL)
    {
        strcpy((char *)fmv, command);
        UnmapViewOfFile(fmv);
    }

    if (fmap != NULL)
    {
        CloseHandle(fmap);
    }

    return 1;
}
