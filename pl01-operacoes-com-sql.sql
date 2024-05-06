-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 24-Fev-2024 às 16:29
-- Versão do servidor: 10.4.32-MariaDB
-- versão do PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `pl01-operacoes-com-sql`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `curso`
--

CREATE TABLE `curso` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `data_inicio` date NOT NULL,
  `data_fim` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `curso`
--

INSERT INTO `curso` (`id`, `nome`, `data_inicio`, `data_fim`) VALUES
(1, 'Data Analyst', '2023-11-23', '2024-06-30'),
(3, 'Software Developer', '2024-03-15', '2024-10-15'),
(4, 'UI/UX Design', '2024-03-01', '2024-04-01'),
(5, 'Marketing Digital', '2024-02-29', '2024-03-30'),
(6, 'Cibersegurança', '2024-03-15', '2024-04-15'),
(7, 'Web Design', '2024-04-05', '2024-07-15'),
(8, 'Python Avançado', '2024-05-15', '2024-10-15'),
(9, 'SQL Basico', '2024-05-10', '2024-09-15'),
(10, 'DAX', '2024-02-26', '2024-03-27');

-- --------------------------------------------------------

--
-- Estrutura da tabela `formando`
--

CREATE TABLE `formando` (
  `id` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `nif` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `formando`
--

INSERT INTO `formando` (`id`, `nome`, `nif`) VALUES
(1, 'Juliana Takahashi', 1),
(2, 'Jose Povinho', 2),
(3, 'Francisco Buarque', 3),
(4, 'Josezito Portugues', 4),
(5, 'Pedro Mendonca', 5),
(6, 'Joca Dondoca', 6),
(7, 'Armindo Lindo', 7),
(8, 'Laura Lampiao', 8),
(9, 'Carla Mandala', 9),
(10, 'Albino Preto', 10),
(12, 'Noemia Tua', 11),
(13, 'Lucas Neto', 12),
(14, 'Vania Betania', 13),
(15, 'Claudia Leite', 14),
(16, 'Francisco Fino', 15),
(17, 'Noberto Alberto', 16),
(18, 'Laura Cabreira', 17);

-- --------------------------------------------------------

--
-- Estrutura da tabela `matricula`
--

CREATE TABLE `matricula` (
  `id` int(11) NOT NULL,
  `formando_id` int(11) NOT NULL,
  `curso_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `matricula`
--

INSERT INTO `matricula` (`id`, `formando_id`, `curso_id`) VALUES
(1, 2, 3),
(2, 4, 3),
(3, 4, 4),
(4, 1, 4),
(5, 3, 3),
(6, 3, 4),
(7, 3, 5),
(8, 6, 6),
(9, 7, 7),
(10, 10, 3),
(11, 13, 5),
(12, 13, 3),
(13, 10, 6),
(14, 1, 8),
(15, 1, 3),
(16, 1, 7),
(17, 14, 5),
(18, 15, 6),
(19, 15, 4),
(20, 16, 6),
(21, 17, 6),
(22, 1, 9),
(23, 1, 6),
(24, 18, 10);

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `curso`
--
ALTER TABLE `curso`
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `formando`
--
ALTER TABLE `formando`
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `matricula`
--
ALTER TABLE `matricula`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `curso`
--
ALTER TABLE `curso`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de tabela `formando`
--
ALTER TABLE `formando`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de tabela `matricula`
--
ALTER TABLE `matricula`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
