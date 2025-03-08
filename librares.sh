#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Checking Python installation ===${NC}"

# Проверка наличия Python
if command -v python3 &>/dev/null; then
    python_version=$(python3 --version)
    echo -e "${GREEN}✓ Python installed: $python_version${NC}"
else
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    exit 1
fi

echo -e "\n${YELLOW}=== Installing required packages ===${NC}"

# Создаем временное окружение для проверки импортов
TMP_DIR=$(mktemp -d)
cd "$TMP_DIR" || exit 1

# Список необходимых пакетов
packages=("requests" "rich")

# Функция для проверки импорта пакета
check_import() {
    if python3 -c "import $1" &>/dev/null; then
        echo -e "${GREEN}✓ Package '$1' successfully installed${NC}"
        return 0
    else
        echo -e "${RED}✗ Failed to import package '$1'${NC}"
        return 1
    fi
}

# Установка и проверка каждого пакета
for package in "${packages[@]}"; do
    echo -e "\n${YELLOW}Installing $package...${NC}"
    python3 -m pip install "$package"
    check_import "$package"
done

echo -e "\n${YELLOW}=== Checking all required imports ===${NC}"
# Финальная проверка всех импортов
all_success=true
for package in "${packages[@]}"; do
    if ! check_import "$package"; then
        all_success=false
    fi
done

# Очистка временного каталога
cd - &>/dev/null
rm -rf "$TMP_DIR"

if [ "$all_success" = true ]; then
    echo -e "\n${GREEN}✓ All dependencies installed successfully!${NC}"
    echo -e "${GREEN}✓ You can now run the program with: python3 main.py${NC}"
else
    echo -e "\n${RED}✗ Some dependencies failed to install. Please check the errors above.${NC}"
    exit 1
fi
